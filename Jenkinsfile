pipeline {
    agent any
    tools {
        maven 'Maven3'
        jdk 'JDK17'
    }
    stages {
        stage('Build') {
            steps {
                bat 'mvn clean compile'
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
      
