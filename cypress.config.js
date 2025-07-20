
const { defineConfig } = require('cypress')

module.exports = defineConfig({
  e2e: {
    baseUrl: process.env.CYPRESS_BASE_URL || 'https://therapy-companion.onrender.com',
    viewportWidth: 1280,
    viewportHeight: 720,
    video: true,
    screenshotOnRunFailure: true,
    
    // Timeouts
    defaultCommandTimeout: 10000,
    requestTimeout: 10000,
    responseTimeout: 10000,
    
    // Retry configuration for CI
    retries: {
      runMode: 2,  // Retry failed tests 2 times in CI
      openMode: 0  // No retries in interactive mode
    },

    // Reporter configuration
    reporter: 'mochawesome',
    reporterOptions: {
      reportDir: 'cypress/results',
      overwrite: false,
      html: true,
      json: true,
      timestamp: 'yyyy-mm-dd_HH-MM-ss',
      charts: true,
      code: true,
      reportTitle: 'Therapy Companion Test Report',
      reportPageTitle: 'Test Results'
    },

    // Environment-specific configuration
    env: {
      // These will be overridden by CI environment variables
      test_user_email: 'default@example.com',
      test_user_password: 'defaultpassword'
    },

    setupNodeEvents(on, config) {
      // Task for logging
      on('task', {
        log(message) {
          console.log(message)
          return null
        },
        table(message) {
          console.table(message)
          return null
        }
      })

      // Load environment-specific config
      const environment = config.env.environment || 'production'
      
      const environmentConfig = {
        development: {
          baseUrl: 'http://localhost:3000'
        },
        staging: {
          baseUrl: 'https://staging.therapy-companion.com'
        },
        production: {
          baseUrl: 'https://therapy-companion.onrender.com'
        }
      }

      // Merge environment config
      if (environmentConfig[environment]) {
        config.baseUrl = environmentConfig[environment].baseUrl
      }

      // Log configuration for debugging
      console.log('Cypress Configuration:')
      console.log('Environment:', environment)
      console.log('Base URL:', config.baseUrl)
      console.log('Browser:', config.browser?.name || 'electron')

      return config
    }
  }
})