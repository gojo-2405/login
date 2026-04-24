def COLOR_MAP = ['SUCCESS': 'good', 'FAILURE': 'danger', 'UNSTABLE': 'danger', 'ABORTED': 'danger']

pipeline {
  agent any

  stages {

    stage('build') {
  steps {
    withCredentials([usernamePassword(
        credentialsId: 'aws-creds',
        usernameVariable: 'AWS_ACCESS_KEY_ID',
        passwordVariable: 'AWS_SECRET_ACCESS_KEY'
    )]) {
      sh '''
      sed -i "s/\\r$//" ./scripts/build
      chmod +x ./scripts/build
      ./scripts/build
      '''
    }
  }
}

    stage('deploy') {
      steps {
        echo 'Deployment is in progress'
        sh '''
        sed -i "s/\\r$//" ./scripts/deploy
        chmod +x ./scripts/deploy
        ./scripts/deploy
        '''
      }
    }
  }

  post {
    always {
      sh 'git show -s --pretty=%an > commit.txt'

      slackSend color: COLOR_MAP[currentBuild.currentResult],
      channel: 'kaaylabs-ci-alerts',
      message: "*${currentBuild.currentResult}:* Job ${env.JOB_NAME}\nAuthor Name:${readFile('commit.txt').trim()} \nBranch name: ${env.BRANCH_NAME}\nBuild number: ${env.BUILD_NUMBER}\nMore info at: ${env.BUILD_URL}"

      cleanWs()
    }
  }
}
