pipeline {
    agent any 

    environment {
        APP_DIR = "/var/www/system_metric_agent"
        DOCKER_FILE_NAME = "Dockerfile"
        DOCKER_HUB_CREDENTIAL = "DOCKER_HUB_CREDENTIAL"
        DOCKER_IMAGE_NAME = "davidaryasetia/system-metrics-agent"
    }

    stages {
        stage ("Checkout the Source Code"){
            steps {
                dir ("${APP_DIR}"){
                    sh """ 
                    git config --global --add safe.directory ${APP_DIR}
                    git pull 
                    """
                }
            }
        }
        stage ("Build Backend system-metrics-agent"){
            steps {
                script {
                    dockerImage = docker.build("${DOCKER_IMAGE_NAME}:latest", "${APP_DIR}")
                }
            }
        }
        stage ("Push image to Dockerhub"){
            steps {
                script {
                    docker.withRegistry("", DOCKER_HUB_CREDENTIAL){
                        dockerImage.push("latest")
                        dockerImage.push("${BUILD_NUMBER}")
                    }
                }
            }
        }
        stage ("Clean up the Jenkins server"){
            steps {
                script {
                    sh "docker rmi ${DOCKER_IMAGE_NAME}:latest || true"
                    sh "docker rmi ${DOCKER_IMAGE_NAME}:${BUILD_NUMBER} || true"
                }
            }
        }
        stage ("Deploy Pull Image and Start Image"){
            steps { 
                dir ("${APP_DIR}"){
                    sh """ 
                    docker compose down 
                    docker compose pull 
                    docker compose up -d 
                    """
                }
            }
        }
    }

    post {
        success {
            echo "Success to deployment App"
        }
        failure {
            echo "Failed to deployment App"
        }
    }
}