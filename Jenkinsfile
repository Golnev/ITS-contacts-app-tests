pipeline {
    agent any
    stages {
        stage('Load Creds') {
            steps {
                withCredentials([
                    string(credentialsId: 'MY_EMAIL', variable: 'MY_EMAIL'),
                    string(credentialsId: 'MY_PASSWORD', variable: 'MY_PASSWORD')
                ]) {
                    script {
                        env.MY_EMAIL = "${MY_EMAIL}"
                        env.MY_PASSWORD = "${MY_PASSWORD}"
                    }
                }
            }
        }
        stage('Build Test Image') {
            steps {
                sh 'docker build -f tests/Dockerfile -t test_runner .'
            }
        }
        stage('Run Tests') {
            steps {
                sh 'docker run --rm test_runner pytest --docker --rm --env email=${env.MY_EMAIL} --env password=&{env.MY_PASSWORD} --browser_name=chrome -m login'
            }
        }
    }
}