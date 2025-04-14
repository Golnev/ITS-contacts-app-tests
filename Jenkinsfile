pipeline {
    agent any
    stages {
        stage('Build Test Image') {
            steps {
                sh 'docker build -t test_runner .'
            }
        }
        stage('Run Tests') {
            steps {
                sh 'docker run --rm test_runner pytest -m --docker auth'
            }
        }
    }
}