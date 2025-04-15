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
                        rm -rf tests/reports/allure-results && mkdir -p tests/reports/allure-results
                        export EMAIL=${EMAIL}
                        export PWD=${PWD}
                        docker run --rm \\
                            -v "\$(pwd)/tests/reports/allure-results:/results" \\
                            test_runner \\
                            sh -c 'pytest \\
                                --docker \\
                                --env email="\$EMAIL" \\
                                --env password="\$PWD" \\
                                --browser_name=chrome \\
                                -m login \\
                                --alluredir=/tmp/allure-results && cp -r /tmp/allure-results/* /results/'
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
