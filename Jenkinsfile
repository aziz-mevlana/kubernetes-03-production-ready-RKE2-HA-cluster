pipeline {
    agent any

    environment {
        DOCKER_IMAGE_REPO = "azizmevlana/django-app"
        DOCKER_CREDENTIALS_ID = "dockerhub-cred"
        KUBECONFIG_CREDENTIALS_ID = "k8s-kubeconfig"
        ARGOCD_APP = "django-app-gitops"
    }

    stages {
        stage('Build & Push Docker Image') {
            steps {
                script {
                    def newTag = env.BUILD_NUMBER
                    dockerImage = docker.build("${DOCKER_IMAGE_REPO}")

                    docker.withRegistry('https://index.docker.io/v1/', "${DOCKER_CREDENTIALS_ID}") {
                        dockerImage.push("${newTag}")
                        dockerImage.push("latest")
                    }
                    env.NEW_TAG = newTag
                }
            }
        }

        stage('Deploy via ArgoCD') {
            steps {
                withCredentials([file(credentialsId: "${KUBECONFIG_CREDENTIALS_ID}", variable: 'KUBECONFIG')]) {
                    sh """
                        # GUVENLIK AGI: override yazmadan once imajin Docker Hub'da gercekten var oldugunu dogrula.
                        # Boylece var olmayan bir tag yuzunden cluster ImagePullBackOff'a girmez.
                        TAG_CODE=\$(curl -s -o /dev/null -w "%{http_code}" \
                          "https://hub.docker.com/v2/repositories/${DOCKER_IMAGE_REPO}/tags/${env.NEW_TAG}")
                        if [ "\$TAG_CODE" != "200" ]; then
                          echo "HATA: ${DOCKER_IMAGE_REPO}:${env.NEW_TAG} Docker Hub'da yok (HTTP \$TAG_CODE). Push stage'ini kontrol et."
                          exit 1
                        fi
                        echo "OK: ${DOCKER_IMAGE_REPO}:${env.NEW_TAG} mevcut, ArgoCD patch uygulaniyor."
                        kubectl -n argocd patch application ${ARGOCD_APP} --type=merge \
                          -p '{"spec":{"source":{"helm":{"parameters":[{"name":"image.tag","value":"${env.NEW_TAG}"}]}}}}'
                    """
                }
            }
        }
    }
}