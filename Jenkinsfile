pipeline {
    agent any

    tools {
        sonarRunner 'SonarQube-Scanner'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('SonarQube') {
                    sh '''
                        sonar-scanner \
                          -Dsonar.projectKey=greenx-dcs-assessment-tool \
                          -Dsonar.projectName="GreenX DCS Assessment Tool" \
                          -Dsonar.sources=GreenX_DCS_Assesment_Tool_Backend,greenX-assessment-tool-frontend
                    '''
                }
            }
        }
    }
}
