pipeline {
    agent any
    stages {
        stage('Setup') {
            steps {
                sh 'python3 -m venv venv'
                sh '. venv/bin/activate'
            }
        }
        stage('Install Dependencies') {
            steps {
                sh 'venv/bin/pip install -r requirements.txt'
            }
        }
        stage('Build') {
            steps {
                sh 'mkdir -p data'
                sh 'venv/bin/python3 data_creation.py'
                sh 'venv/bin/python3 data_preprocessing.py'
                sh 'venv/bin/python3 model_preparation.py'
                sh 'venv/bin/python3 model_testing.py'
            }
        }
        stage('Unit Tests') {
            steps {
                sh 'venv/bin/python3 -m unittest discover -s tests -p "test_*.py"'
            }
        }
        //stage('PEP8 Compliance Check') {
        //    steps {
        //        sh 'venv/bin/flake8 --filename=*.py --exclude=venv /var/jenkins_home/workspace/CI-CD/'
        //    }
        //}
        stage('Deploy morda') {
            steps {
                sh 'sudo docker run -it --detach $(sudo docker build -q .)'
            }
        }
    }
}
