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
                ])
                sh """
                        docker run --rm \
                            -e email="${EMAIL}" \
                            -e password="${PWD}" \
                            --docker
                            pytest --browser_name=chrome -m login
                    """
            }
        }
    }
}