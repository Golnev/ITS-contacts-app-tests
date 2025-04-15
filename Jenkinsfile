pipeline {
    agent any
    stages {
        stage('Build Test Image') {
            steps {
                sh 'docker build -f tests/Dockerfile -t test_runner .'
            }
        }
        stage('Prepare') {
            steps {
                sh 'mkdir -p tests/reports/allure-results && chmod -R 777 tests/reports'
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
                            -v ${WORKSPACE}/tests/reports/allure-results:/app/tests/reports/allure-results \
                            test_runner \
                            pytest \
                            --docker \
                            --env email="$EMAIL" \
                            --env password="$PWD" \
                            --browser_name=chrome \
                            -m login

                        docker cp test_container:/app/tests/reports/allure-results/. ./tests/reports/allure-results/ || true
                        docker rm -f test_container || true

                    """
                }
            }
        }
        stage('Publish Allure Report') {
            steps {
                script {
                    def hasResults = fileExists 'tests/reports/allure-results'
                    if (hasResults) {
                        allure includeProperties: false,
                               jdk: '',
                               results: [[path: 'tests/reports/allure-results']],
                               reportBuildPolicy: 'ALWAYS'
                    } else {
                        echo 'Warning: No Allure results found'
                    }
                }
            }
        }
    }
    post {
        always {
            archiveArtifacts artifacts: 'tests/reports/allure-results/**', allowEmptyArchive: true
        }
    }
}
