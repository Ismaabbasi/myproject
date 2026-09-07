pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Tests + Coverage') {
            steps {
                sh '''
                    set -e

                    echo "======================================"
                    echo "Starting temporary MySQL for tests"
                    echo "======================================"

                    docker network inspect greenx-ci-network >/dev/null 2>&1 || \
                        docker network create greenx-ci-network

                    docker rm -f greenx-test-mysql >/dev/null 2>&1 || true

                    docker run -d \
                        --name greenx-test-mysql \
                        --network greenx-ci-network \
                        -e MYSQL_DATABASE=test-fca \
                        -e MYSQL_USER=greenx \
                        -e MYSQL_PASSWORD=testpass \
                        -e MYSQL_ROOT_PASSWORD=rootpass \
                        mysql:8.0

                    echo "Waiting for MySQL..."

                    for i in $(seq 1 30); do
                        if docker exec greenx-test-mysql \
                            mysqladmin ping -h 127.0.0.1 -u root -prootpass --silent; then
                            echo "MySQL is ready"
                            break
                        fi

                        if [ "$i" -eq 30 ]; then
                            echo "MySQL failed to start"
                            docker logs greenx-test-mysql
                            exit 1
                        fi

                        sleep 2
                    done

                    echo "======================================"
                    echo "Running backend tests"
                    echo "======================================"

                    docker run --rm \
                        --network greenx-ci-network \
                        -v "$WORKSPACE":/workspace \
                        -w /workspace/GreenX_DCS_Assesment_Tool_Backend \
                        -e ENV=test \
                        -e DB=mysql \
                        -e DB_USER=greenx \
                        -e DB_PASSWORD=testpass \
                        -e DB_HOST=greenx-test-mysql \
                        -e DB_PORT=3306 \
                        -e SECRET_KEY=ci-test-secret-key-123456789 \
                        python:3.11-slim \
                        bash -c '
                            pip install --no-cache-dir -r requirements.txt pytest coverage &&
                            pytest -q --cov=app --cov-report=xml
                        '

                    echo "======================================"
                    echo "Coverage file"
                    echo "======================================"

                    test -f GreenX_DCS_Assesment_Tool_Backend/coverage.xml

                    grep -o "line-rate=\"[^\"]*\"" \
                        GreenX_DCS_Assesment_Tool_Backend/coverage.xml | head -1

                    echo "======================================"
                    echo "Removing temporary MySQL"
                    echo "======================================"

                    docker rm -f greenx-test-mysql >/dev/null 2>&1 || true
                '''
            }

            post {
                always {
                    sh '''
                        docker rm -f greenx-test-mysql >/dev/null 2>&1 || true
                    '''
                }
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
                            -Dsonar.sources="GreenX_DCS_Assesment_Tool_Backend,greenX-assessment-tool-frontend" \
                            -Dsonar.tests="GreenX_DCS_Assesment_Tool_Backend/tests" \
                            -Dsonar.python.version=3.11 \
                            -Dsonar.python.coverage.reportPaths=GreenX_DCS_Assesment_Tool_Backend/coverage.xml
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
                sh '''
                    echo "======================================"
                    echo "Building Backend Image"
                    echo "======================================"

                    docker build \
                        -t myproject-backend:latest \
                        ./GreenX_DCS_Assesment_Tool_Backend

                    echo "======================================"
                    echo "Building Frontend Image"
                    echo "======================================"

                    docker build \
                        -t myproject-frontend:latest \
                        ./greenX-assessment-tool-frontend
                '''
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
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-credentials',
                        usernameVariable: 'DOCKERHUB_USERNAME',
                        passwordVariable: 'DOCKERHUB_TOKEN'
                    )
                ]) {
                    sh '''
                        echo "$DOCKERHUB_TOKEN" | \
                            docker login \
                            -u "$DOCKERHUB_USERNAME" \
                            --password-stdin

                        docker tag \
                            myproject-backend:latest \
                            $DOCKERHUB_USERNAME/myproject-backend:latest

                        docker tag \
                            myproject-frontend:latest \
                            $DOCKERHUB_USERNAME/myproject-frontend:latest

                        docker push \
                            $DOCKERHUB_USERNAME/myproject-backend:latest

                        docker push \
                            $DOCKERHUB_USERNAME/myproject-frontend:latest

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
