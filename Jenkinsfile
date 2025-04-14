pipeline {
    agent any
    stages {
        stage('Build Test Image') {
            steps {
                sh 'sudo docker build -f tests/Dockerfile -t test_runner .'
            }
        }
        stage('Run Tests') {
            steps {
                sh 'sudo docker run --rm test_runner pytest -m --docker auth'
            }
        }
    }
}