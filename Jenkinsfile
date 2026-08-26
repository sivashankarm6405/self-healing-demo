pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                echo 'Simulating a build step...'
                bat 'exit /b 1'
            }
        }
    }
    post {
        failure {
            echo "Pipeline failed — this is where the healing script will run"
        }
        success {
            echo "Pipeline succeeded — no action required"
        }
    }
}
      
