pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub')
        DOCKERHUB_USER = 'yash0010'
        FRONTEND_IMAGE = "${DOCKERHUB_USER}/anpr-frontend"
        BACKEND_IMAGE = "${DOCKERHUB_USER}/anpr-backend"
        VERSION = "${env.BUILD_NUMBER}"
        FRONTEND_TAG = "${VERSION}"
        BACKEND_TAG = "${VERSION}"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'release', url: 'https://github.com/yashwanth0010/ANPR.git'
            }
        }

        stage('Build Backend Image') {
            steps {
                script {
                    sh """
                        docker build -t ${BACKEND_IMAGE}:${BACKEND_TAG} ./backend
                    """
                }
            }
        }

        stage('Build Frontend Image') {
            steps {
                script {
                    sh """
                        docker build -t ${FRONTEND_IMAGE}:${FRONTEND_TAG} ./frontend
                    """
                }
            }
        }

        stage('Push Images to Docker Hub') {
            steps {
                script {
                        sh """
                             echo ${DOCKERHUB_CREDENTIALS_PSW} | docker login -u ${DOCKERHUB_CREDENTIALS_USR} --password-stdin
                            docker push ${BACKEND_IMAGE}:${BACKEND_TAG}
                            docker push ${FRONTEND_IMAGE}:${FRONTEND_TAG}
                        """
                    }
                }
            }
        }

        stage('Cleanup') {
            steps {
                sh """
                    docker rmi ${BACKEND_IMAGE}:${BACKEND_TAG} || true
                    docker rmi ${FRONTEND_IMAGE}:${FRONTEND_TAG} || true
                """
            }
        }
    }

    post {
        success {
            echo "✅ Successfully built and pushed images to Docker Hub!"
        }
        failure {
            echo "❌ Build failed. Check logs."
        }
    }
}
