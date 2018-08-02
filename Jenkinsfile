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
          steps {
            stash includes: '*', name: 'file'
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
            unstash 'file'
          }
        }
        stage('run_script') {
          agent {
            node {
              label 'win7_64_1'
              withPythonEnv('/usr/bin/python3.5') {
                    pysh 'C:\\jenkins\\workspace\\test_from_vm\\.pyenv-usr-bin-python3.5\\bin\\python3.5'
                }
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
