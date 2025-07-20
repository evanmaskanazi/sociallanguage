describe('Therapy Companion Integration Tests', () => {
  // Test credentials - update cypress.env.json instead of hardcoding
  const credentials = {
    email: Cypress.env('test_user_email') || 'fallback@email.com',
    password: Cypress.env('test_user_password') || 'fallbackPassword'
  }

  it('should navigate from homepage to login', () => {
    // Start at homepage
    cy.visit('https://therapy-companion.onrender.com')
    
    // Click Get Started to go to login
    cy.contains('a', 'Get Started').click()
    
    // Verify we're on login page
    cy.url().should('include', '/login.html')
  })

  it('should login successfully', () => {
    // Go directly to login
    cy.visit('https://therapy-companion.onrender.com/login.html')
    
    // Use specific IDs for login form
    cy.get('#loginEmail').clear().type(credentials.email)
    cy.get('#loginPassword').clear().type(credentials.password)
    
    // Click the correct login button
    cy.get('button[type="submit"]').contains('Login').click()
    
    // Verify successful login
    cy.url().should('not.include', '/login.html', { timeout: 10000 })
    
    // Add assertions for dashboard elements
    // cy.contains('Dashboard').should('be.visible')
    // cy.contains('Welcome').should('be.visible')
  })

  it('should complete full user flow', () => {
    // Homepage -> Login -> Dashboard
    cy.visit('https://therapy-companion.onrender.com')
    cy.contains('a', 'Get Started').click()
    
    // Login
    cy.get('#loginEmail').type(credentials.email)
    cy.get('#loginPassword').type(credentials.password)
    cy.get('button[type="submit"]').contains('Login').click()
    
    // Verify we reached dashboard
    cy.url().should('not.include', '/login.html')
    
    // Add more integration tests here
    // e.g., navigate to different sections, test features
  })
})