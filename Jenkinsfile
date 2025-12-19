pipeline {
  agent any

  options {
    timestamps()
    disableConcurrentBuilds()
    skipDefaultCheckout(true)
  }

  environment {
    APP_URL = "http://127.0.0.1:5000"
    COMPOSE_FILE = "docker-compose.yml"
  }

  stages {
    stage('Checkout') {
      steps {
        cleanWs()
        checkout scm
        sh '''
          set -e
          echo "WORKSPACE = $WORKSPACE"
          pwd
          ls -la
          echo "Listing compose file:"
          ls -la "$COMPOSE_FILE"
        '''
      }
    }

    stage('Build & Deploy (Docker Compose)') {
      steps {
        dir("${WORKSPACE}") {
          sh '''
            set -e
            echo "Running docker compose in: $(pwd)"
            docker compose -f "$COMPOSE_FILE" down || true
            docker compose -f "$COMPOSE_FILE" up -d --build
          '''
        }
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
          docker ps || true
          docker compose -f "$COMPOSE_FILE" logs --tail=120 || true
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
      sh 'docker compose -f docker-compose.yml logs --tail=200 || true'
    }
  }
}
