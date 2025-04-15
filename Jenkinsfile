pipeline {
    agent any
    stages {
        stage('Prepare') {
            steps {
                sh 'mkdir -p tests/reports/allure-results && chmod -R 777 tests/reports'
            }
        }

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
                        docker run \
                            test_runner \
                            pytest \
                            --docker \
                            --env email="$EMAIL" \
                            --env password="$PWD" \
                            --browser_name=chrome \
                            -m login

                        docker cp test_container:/app/tests/reports/allure-results ./tests/reports/
                        docker rm test_container

                    """
                }
            }
        }
        stage('Publish Allure Report') {
            steps {
                allure includeProperties: false, jdk: '', results: [[path: 'tests/reports/allure-results']], reportBuildPolicy: 'ALWAYS'
            }
        }
    }
    post {
        always {
            archiveArtifacts artifacts: 'tests/reports/allure-results/**', allowEmptyArchive: true
        }
    }
}
