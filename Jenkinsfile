pipeline {
  agent any
  stages {
    stage('Prepare') {
      parallel {
        stage('get_git') {
          agent any
          steps {
            git(url: 'https://github.com/widoc84/test1_acIdcfg.git', branch: 'master', changelog: true)
          }
        }
        stage('archive_files') {
          agent any
          steps {
            sh 'stash includes: \'**\', name: \'file\', useDefaultExcludes: false'
          }
        }
      }
    }
    stage('run') {
      parallel {
        stage('dearchive_files') {
          agent {
            node {
              label 'win7_64_1'
            }
            
          }
          steps {
            sh 'unstash \'file\''
          }
        }
        stage('run_script') {
          agent {
            node {
              label 'win7_64_1'
            }
            
          }
          steps {
            sh '1'
          }
        }
      }
    }
  }
}