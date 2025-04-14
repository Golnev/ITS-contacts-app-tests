pipeline {
    agent any
    stages {
        stage('Build Test Image') {
            steps {
                sh 'docker build -f tests/Dockerfile -t test_runner .'
            }
        }
        stage('Run Tests') {
            steps {
                sh 'docker run --rm test_runner pytest --docker --rm -m auth --env email=myemail@example.com --env password=zaq1@WSX'
            }
        }
    }
}