pipeline {
    agent any
    tools {
        maven 'Maven3'
        jdk 'JDK17'
    }
    stages {
        stage('Build') {
            steps {
                script {
                    def status = bat(script: 'mvn clean compile > build.log 2>&1', returnStatus: true)
                    if (status != 0) {
                        error("Build failed — see build.log")
                    }
                }
            }
        }
    }
    post {
        failure {
            echo "Pipeline failed — running healing script"
            bat '"C:\\Users\\muthu\\AppData\\Local\\Programs\\Python\\Python313\\python.exe" healing_script.py'
        }
        success {
            echo "Pipeline succeeded — no action required"
        }
    }
}
      
