pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('SonarQube Analysis') {
            steps {
                script {
                    def scannerHome = tool(
                        name: 'SonarQube-Scanner',
                        type: 'hudson.plugins.sonar.SonarRunnerInstallation'
                    )

                    withSonarQubeEnv('SonarQube') {
                        sh """
                            ${scannerHome}/bin/sonar-scanner \
                            -Dsonar.projectKey=GreenX-DCS-Assessment-Tool \
                            -Dsonar.projectName="GreenX DCS Assessment Tool" \
                            -Dsonar.sources="GreenX_DCS_Assesment_Tool_Backend,greenX-assessment-tool-frontend"
                        """
                    }
                }
            }
        }

        stage('Quality Gate') {
            steps {
                timeout(time: 5, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }

        stage('Build Docker Images') {
            steps {
                sh 'docker build -t myproject-backend:latest ./GreenX_DCS_Assesment_Tool_Backend'
                sh 'docker build -t myproject-frontend:latest ./greenX-assessment-tool-frontend'
            }
        }

        stage('Trivy Security Scan') {
            steps {
                sh '''
                    echo "======================================"
                    echo "Trivy Backend Security Scan"
                    echo "======================================"

                    trivy image \
                        --scanners vuln \
                        --ignore-unfixed \
                        --severity HIGH,CRITICAL \
                        --exit-code 0 \
                        myproject-backend:latest

                    echo "======================================"
                    echo "Trivy Frontend Security Scan"
                    echo "======================================"

                    trivy image \
                        --scanners vuln \
                        --ignore-unfixed \
                        --severity HIGH,CRITICAL \
                        --exit-code 0 \
                        myproject-frontend:latest
                '''
            }
        }

        stage('Push Docker Images') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-credentials',
                    usernameVariable: 'DOCKERHUB_USERNAME',
                    passwordVariable: 'DOCKERHUB_TOKEN'
                )]) {
                    sh '''
                        echo "$DOCKERHUB_TOKEN" | docker login -u "$DOCKERHUB_USERNAME" --password-stdin

                        docker tag myproject-backend:latest $DOCKERHUB_USERNAME/myproject-backend:latest
                        docker tag myproject-frontend:latest $DOCKERHUB_USERNAME/myproject-frontend:latest

                        docker push $DOCKERHUB_USERNAME/myproject-backend:latest
                        docker push $DOCKERHUB_USERNAME/myproject-frontend:latest

                        docker logout
                    '''
                }
            }
        }

        stage('Deploy to EC2') {
            steps {
                sh '''
                    cd /opt/myproject/myproject

                    docker compose pull backend frontend

                    docker compose up -d backend frontend
                '''
            }
        }
    }
}
