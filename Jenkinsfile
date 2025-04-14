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
                        docker run --rm \
                            -v "\$WORKSPACE/tests/reports:/app/tests/reports/allure-results" \
                            test_runner \
                            pytest \
                            --docker \
                            --env email="$EMAIL" \
                            --env password="$PWD" \
                            --browser_name=chrome \
                            -m login \
                            --alluredir=tests/reports/allure-results
                        """
                }
            }
        }
        stage('Publish Allure Report') {
            steps {
                allure includeProperties: false, jdk: '', results: [[path: 'tests/reports/allure-results']]
            }
        }
    }
}