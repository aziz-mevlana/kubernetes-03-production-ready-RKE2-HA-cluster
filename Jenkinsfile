pipeline {
    agent any

    environment {
        DOCKER_IMAGE_REPO = "azizmevlana/django-app"
        DOCKER_CREDENTIALS_ID = "dockerhub-cred"
        GIT_CREDENTIALS_ID = "github-cred"
        CHART_VALUES = "deployments/django-chart/values.yaml"
    }

    stages {
        stage('Build & Push Docker Image') {
            steps {
                script {
                    // GitOps için benzersiz ve izlenebilir imaj etiketi kullan (Jenkins build numarası)
                    def newTag = env.BUILD_NUMBER
                    dockerImage = docker.build("${DOCKER_IMAGE_REPO}")

                    docker.withRegistry('https://index.docker.io/v1/', "${DOCKER_CREDENTIALS_ID}") {
                        dockerImage.tag("${newTag}")
                        dockerImage.push()
                        dockerImage.push("latest")
                    }

                    // Chart values içindeki imaj etiketini güncelle -> ArgoCD auto-sync'i tetikler
                    sh "sed -i \"s|tag: \\\"latest\\\"|tag: \\\"${newTag}\\\"|\" ${CHART_VALUES}"
                }
            }
        }

        stage('Trigger ArgoCD via Git') {
            steps {
                withCredentials([gitUsernamePassword(
                    credentialsId: "${GIT_CREDENTIALS_ID}",
                    usernameVariable: 'GIT_USER',
                    passwordVariable: 'GIT_PASS'
                )]) {
                    sh """
                        git config user.email "jenkins@localhost"
                        git config user.name "Jenkins CI"
                        git add ${CHART_VALUES}
                        git commit -m "chore: bump django-app image tag to ${env.BUILD_NUMBER}"
                        git push origin HEAD
                    """
                }
            }
        }
    }
}