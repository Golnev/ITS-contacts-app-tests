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
                withCredentials([
                    string(credentialsId: 'MY_EMAIL', variable: 'EMAIL'),
                    string(credentialsId: 'MY_PASSWORD', variable: 'PWD')
                ]) {
                    sh """
                        docker run --rm test_runner \
                            pytest \
                            --docker \
                            --rm \
                            --env email="$EMAIL" \
                            --env password="$PWD" \
                            --browser_name=chrome \
                            -m login
                    """
                }
            }
        }
        stage('Publish Allure Report') {
            steps {
                allure includeProperties: false, jdk: '', results: [[path: 'allure-results']]
            }
        }
    }
}