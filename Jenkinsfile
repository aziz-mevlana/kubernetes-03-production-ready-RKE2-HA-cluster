pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = "<DOCKERHUB_KULLANICI_ADIN>/django-app:latest"
        DOCKER_CREDENTIALS_ID = "dockerhub-cred"
        KUBECONFIG_CREDENTIALS_ID = "k8s-kubeconfig"
    }
    
    stages {
        stage('Build Docker Image') {
            steps {
                script {
                    dockerImage = docker.build("${DOCKER_IMAGE}")
                }
            }
        }
        
        stage('Push Docker Image') {
            steps {
                script {
                    docker.withRegistry('https://index.docker.io/v1/', "${DOCKER_CREDENTIALS_ID}") {
                        dockerImage.push()
                    }
                }
            }
        }
        
        stage('Deploy to RKE2') {
            steps {
                withCredentials([file(credentialsId: "${KUBECONFIG_CREDENTIALS_ID}", variable: 'KUBECONFIG')]) {
                    sh 'kubectl apply -f k8s/deployment.yaml'
                    sh 'kubectl apply -f k8s/service.yaml'
                    sh 'kubectl apply -f k8s/ingress.yaml'
                    sh 'kubectl rollout restart deployment/django-app'
                }
            }
        }
    }
}
