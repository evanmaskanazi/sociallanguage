pipeline {
    agent any
    
    environment {
        // Set Node.js path
        NODEJS_HOME = "${tool 'NodeJS-18'}"
        PATH = "${env.NODEJS_HOME}/bin:${env.PATH}"
        
        // Cypress environment variables
        CYPRESS_CACHE_FOLDER = "${WORKSPACE}/.cypress-cache"
        CYPRESS_BASE_URL = credentials('cypress-base-url')
        CYPRESS_TEST_USER_EMAIL = credentials('cypress-test-email')
        CYPRESS_TEST_USER_PASSWORD = credentials('cypress-test-password')
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Install Dependencies') {
            steps {
                script {
                    // Clean install
                    bat 'npm ci'
                    
                    // Verify Cypress installation
                    bat 'npx cypress verify'
                }
            }
        }
        
        stage('Run Tests - Chrome') {
            steps {
                script {
                    try {
                        bat 'npm run cypress:run:chrome'
                    } catch (Exception e) {
                        currentBuild.result = 'UNSTABLE'
                    }
                }
            }
        }
        
        stage('Run Tests - Edge') {
            when {
                expression { isUnix() }
            }
            steps {
                script {
                    try {
                        bat 'npm run cypress:run:edge'
                    } catch (Exception e) {
                        currentBuild.result = 'UNSTABLE'
                    }
                }
            }
        }
        
        stage('Generate Reports') {
            steps {
                script {
                    // Merge JSON reports
                    bat 'npm run report:merge'
                    
                    // Generate HTML report
                    bat 'npm run report:generate'
                }
            }
        }
        
        stage('Archive Results') {
            steps {
                // Archive test results
                archiveArtifacts artifacts: 'cypress/results/*.html', allowEmptyArchive: true
                archiveArtifacts artifacts: 'cypress/screenbatots/**/*.png', allowEmptyArchive: true
                archiveArtifacts artifacts: 'cypress/videos/**/*.mp4', allowEmptyArchive: true
                
                // Publibat HTML report
                publibatHTML([
                    allowMissing: false,
                    alwaysLinkToLastBuild: true,
                    keepAll: true,
                    reportDir: 'cypress/results',
                    reportFiles: 'report.html',
                    reportName: 'Cypress Test Report',
                    reportTitles: 'E2E Test Results'
                ])
                
                // Publibat test results for trends
                junit 'cypress/results/*.xml'
            }
        }
    }
    
    post {
        always {
            // Clean workspace
            cleanWs()
        }
        
        failure {
            // Send notification on failure
            emailext (
                subject: "Cypress Tests Failed: ${env.JOB_NAME} - ${env.BUILD_NUMBER}",
                body: """
                    <p>Cypress tests failed for ${env.JOB_NAME} build ${env.BUILD_NUMBER}</p>
                    <p>Check the test report: ${env.BUILD_URL}Cypress_20Test_20Report</p>
                """,
                to: "${env.CHANGE_AUTHOR_EMAIL}",
                mimeType: 'text/html'
            )
        }
        
        unstable {
            // Send notification on unstable
            emailext (
                subject: "Cypress Tests Unstable: ${env.JOB_NAME} - ${env.BUILD_NUMBER}",
                body: """
                    <p>Some Cypress tests failed for ${env.JOB_NAME} build ${env.BUILD_NUMBER}</p>
                    <p>Check the test report: ${env.BUILD_URL}Cypress_20Test_20Report</p>
                """,
                to: "${env.CHANGE_AUTHOR_EMAIL}",
                mimeType: 'text/html'
            )
        }
    }
}