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
                    // Benzersiz ve izlenebilir imaj etiketi (Jenkins build numarası)
                    def newTag = env.BUILD_NUMBER
                    dockerImage = docker.build("${DOCKER_IMAGE_REPO}")

                    docker.withRegistry('https://index.docker.io/v1/', "${DOCKER_CREDENTIALS_ID}") {
                        dockerImage.tag("${newTag}")
                        dockerImage.push()
                        dockerImage.push("latest")
                    }

                    // Yeni tag'i sonraki stage'de kullanabilmek için sakla
                    env.NEW_TAG = newTag
                }
            }
        }

        stage('Deploy via ArgoCD') {
            steps {
                withCredentials([file(credentialsId: "${KUBECONFIG_CREDENTIALS_ID}", variable: 'KUBECONFIG')]) {
                    sh """
                        kubectl -n argocd patch application ${ARGOCD_APP} --type=merge \
                          -p '{"spec":{"source":{"helm":{"parameters":[{"name":"image.tag","value":"${env.NEW_TAG}"}]}}}}'
                    """
                }
            }
        }
    }
}