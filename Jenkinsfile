pipeline {
  agent any

  options {
    timestamps()
    disableConcurrentBuilds()
  }

  environment {
    APP_URL = "http://127.0.0.1:5000"
  }

  stages {
    stage('Checkout') {
      steps {
        cleanWs()
        checkout scm
      }
    }

    stage('Build & Deploy (Docker Compose)') {
      steps {
        sh '''
          set -e
          docker compose down || true
          docker compose up -d --build
        '''
      }
    }

    stage('Healthcheck') {
      steps {
        sh '''
          set -e
          echo "Waiting for app to become ready..."
          for i in $(seq 1 20); do
            if curl -fsS http://127.0.0.1:5000/ >/dev/null; then
              echo "APP is UP"
              exit 0
            fi
            echo "Not ready yet... attempt $i"
            sleep 2
          done
          echo "APP did not become ready"
          docker ps
          docker compose logs --tail=80
          exit 1
        '''
      }
    }
  }

  post {
    always {
      sh 'docker ps || true'
    }
    failure {
      sh 'docker compose logs --tail=120 || true'
    }
  }
}
