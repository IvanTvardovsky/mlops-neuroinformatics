pipeline {
    agent any
    stages {
        stage('Setup') {
            steps {
                sh 'python3 -m venv venv'
                sh '. venv/bin/activate'
                sh 'git clone https://github.com/IvanTvardovsky/mlops-neuroinformatics.git'
            }
        }
        stage('Install Dependencies') {
            steps {
                dir('mlops-neuroinformatics'){
                    sh '../venv/bin/pip install -r requirements.txt'
                }
            }
        }
        stage('Build') {
            steps {
                dir('mlops-neuroinformatics'){
                    sh 'mkdir -p data'
                    sh '../venv/bin/python3 data_initializer.py'
                    sh '../venv/bin/python3 data_transformer.py'
                    sh '../venv/bin/python3 model_constructor.py'
                    sh '../venv/bin/python3 model_tester.py'
                }
            }
        }
        stage('Unit Tests') {
            steps {
                dir('mlops-neuroinformatics'){
                    sh '../venv/bin/python3 -m unittest discover -s tests -p "test_*.py"'
                }
            }
        }
        //stage('PEP8 Compliance Check') {
        //    steps {
        //        dir('mlops-neuroinformatics'){
        //            sh 'venv/bin/flake8 --filename=*.py --exclude=venv /var/jenkins_home/workspace/CI-CD/'
        //        }
        //    }
        //}
        stage('Deploy morda') {
            steps {
                dir('mlops-neuroinformatics'){
                    sh 'sudo docker stop $(sudo docker container ls -q)'
                    sh 'sudo docker run -it -p 1488:1488--detach $(sudo docker build -q .)'
                }
            }
        }
        stage('Cleanup') {
            steps{
                sh 'rm -rf mlops-neuroinformatics'
                sh 'rm -rf venv'
            }
        }
    }
}
