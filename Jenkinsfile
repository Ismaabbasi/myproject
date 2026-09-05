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
                          -Dsonar.sources=GreenX_DCS_Assesment_Tool_Backend,greenX-assessment-tool-frontend
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
}
