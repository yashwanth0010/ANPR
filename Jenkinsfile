pipeline {
    agent any

    environment {
        // DockerHub credentials ID (create in Jenkins → Credentials)
        DOCKERHUB_CREDENTIALS = credentials('dockerhub')
        // Replace with your DockerHub username and repo name
        IMAGE_NAME = 'yash0010/anpr'
    }

    stages {
        stage('Build Docker Image') {
            steps {
                script {
                    // Create a simple version tag
                    COMMIT_HASH = sh(script: "git rev-parse --short HEAD", returnStdout: true).trim()
                    VERSION_TAG = "${BUILD_NUMBER}-${COMMIT_HASH}"

                    echo "🚧 Building Docker image: ${IMAGE_NAME}:${VERSION_TAG}"
                    sh """
                        docker build -t ${IMAGE_NAME}:${VERSION_TAG} -t ${IMAGE_NAME}:latest .
                    """
                }
            }
        }

        stage('Push to DockerHub') {
            steps {
                script {
                    echo "📦 Pushing image ${IMAGE_NAME}:${VERSION_TAG} to DockerHub..."
                    sh """
                        echo ${DOCKERHUB_CREDENTIALS_PSW} | docker login -u ${DOCKERHUB_CREDENTIALS_USR} --password-stdin
                        docker push ${IMAGE_NAME}:${VERSION_TAG}
                        docker push ${IMAGE_NAME}:latest
                    """
                }
            }
        }

        stage('Clean Up') {
            steps {
                script {
                    echo "🧹 Cleaning up local images..."
                    sh "docker rmi ${IMAGE_NAME}:${VERSION_TAG} ${IMAGE_NAME}:latest || true"
                }
            }
        }
    }

    post {
        success {
            echo "✅ Successfully built and pushed image: ${IMAGE_NAME}:${VERSION_TAG}"
        }
        failure {
            echo "❌ Build failed — check console output for errors."
        }
    }
}
