pipeline {
    agent any

    stages {

        // =========================================================
        // 1. CHECKOUT
        // =========================================================
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        // =========================================================
        // 2. TESTS + COVERAGE
        // =========================================================
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
                            mysqladmin ping \
                            -h 127.0.0.1 \
                            -u root \
                            -prootpass \
                            --silent; then

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
                        -e SECRET_KEY=ci-test-secret-key-12345678901234567890 \
                        python:3.11-slim \
                        bash -c '
                            set -e

                            apt-get update

                            apt-get install -y \
                                gcc \
                                g++ \
                                libc6-dev \
                                libffi-dev

                            pip install --no-cache-dir -r requirements.txt

                            pip install --no-cache-dir pytest coverage

                            pytest -q \
                                --cov=app \
                                --cov-report=xml
                        '

                    echo "======================================"
                    echo "Checking coverage file"
                    echo "======================================"

                    test -f GreenX_DCS_Assesment_Tool_Backend/coverage.xml

                    echo "Coverage file exists:"
                    ls -lh GreenX_DCS_Assesment_Tool_Backend/coverage.xml
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

        // =========================================================
        // 3. SONARQUBE ANALYSIS
        // =========================================================
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

        // =========================================================
        // 4. QUALITY GATE
        // =========================================================
        stage('Quality Gate') {
            steps {

                timeout(time: 5, unit: 'MINUTES') {

                    waitForQualityGate abortPipeline: true
                }
            }
        }

        // =========================================================
        // 5. BUILD DOCKER IMAGES
        // =========================================================
        stage('Build Docker Images') {
            steps {
                sh '''
                    set -e

                    echo "======================================"
                    echo "Building Backend Docker Image"
                    echo "======================================"

                    docker build \
                        -t myproject-backend:latest \
                        ./GreenX_DCS_Assesment_Tool_Backend

                    echo "======================================"
                    echo "Building Frontend Docker Image"
                    echo "======================================"

                    docker build \
                        -t myproject-frontend:latest \
                        ./greenX-assessment-tool-frontend

                    echo "======================================"
                    echo "Docker Images Built Successfully"
                    echo "======================================"

                    docker images | grep myproject
                '''
            }
        }

        // =========================================================
        // 6. TRIVY SECURITY SCAN
        // =========================================================
        stage('Trivy Security Scan') {
            steps {
                sh '''
                    set -e

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

                    echo "======================================"
                    echo "Trivy Security Scan Completed"
                    echo "======================================"
                '''
            }
        }

        // =========================================================
        // 7. PUSH DOCKER IMAGES
        // =========================================================
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
                        set -e

                        echo "======================================"
                        echo "Logging in to Docker Hub"
                        echo "======================================"

                        echo "$DOCKERHUB_TOKEN" | \
                            docker login \
                            -u "$DOCKERHUB_USERNAME" \
                            --password-stdin

                        echo "======================================"
                        echo "Tagging Backend Image"
                        echo "======================================"

                        docker tag \
                            myproject-backend:latest \
                            "$DOCKERHUB_USERNAME/myproject-backend:latest"

                        echo "======================================"
                        echo "Tagging Frontend Image"
                        echo "======================================"

                        docker tag \
                            myproject-frontend:latest \
                            "$DOCKERHUB_USERNAME/myproject-frontend:latest"

                        echo "======================================"
                        echo "Pushing Backend Image"
                        echo "======================================"

                        docker push \
                            "$DOCKERHUB_USERNAME/myproject-backend:latest"

                        echo "======================================"
                        echo "Pushing Frontend Image"
                        echo "======================================"

                        docker push \
                            "$DOCKERHUB_USERNAME/myproject-frontend:latest"

                        echo "======================================"
                        echo "Docker Images Pushed Successfully"
                        echo "======================================"

                        docker logout
                    '''
                }
            }
        }

        // =========================================================
        // 8. DEPLOY TO EC2
        // =========================================================
        stage('Deploy to EC2') {
            steps {
                sh '''
                    set -e

                    echo "======================================"
                    echo "Deploying Application to EC2"
                    echo "======================================"

                    cd /opt/myproject/myproject

                    echo "Pulling latest backend image..."
                    docker compose pull backend

                    echo "Pulling latest frontend image..."
                    docker compose pull frontend

                    echo "Starting backend and frontend..."
                    docker compose up -d backend frontend

                    echo "======================================"
                    echo "Deployment Completed"
                    echo "======================================"

                    docker compose ps
                '''
            }
        }
    }

    // =============================================================
    // POST ACTIONS
    // =============================================================
    post {

        success {
            echo "======================================"
            echo "CI/CD PIPELINE COMPLETED SUCCESSFULLY"
            echo "======================================"
        }

        failure {
            echo "======================================"
            echo "CI/CD PIPELINE FAILED"
            echo "Check the failed stage above."
            echo "======================================"
        }
    }
}


