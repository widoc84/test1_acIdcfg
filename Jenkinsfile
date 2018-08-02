pipeline {
  agent any
  stages {
    stage('Prepare') {
      parallel {
        stage('Prepare') {
          steps {
            git(url: 'https://github.com/widoc84/test1_acIdcfg.git', branch: 'master')
          }
        }
        stage('') {
          steps {
            pybat(script: 'testscript.py', returnStatus: true, returnStdout: true)
          }
        }
      }
    }
  }
}