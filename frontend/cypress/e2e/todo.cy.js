describe('Todo list', () => {
  let uid;
  let email;

  before(function () {
    // Create a user via API
    cy.fixture('user.json')
      .then((user) => {
        cy.request({
          method: 'POST',
          url: `http://localhost:${Cypress.env('REACT_APP_BACKEND_PORT') || 5000}/users/create`,
          form: true,
          body: user
        }).then((response) => {
          uid = response.body._id.$oid;
          email = user.email;
        });
      });
  });

  beforeEach(function () {
    // Log in before each test
    cy.visit('/login')
    cy.get('input#email').type(email);
    cy.get('form').submit();
    cy.get('h1').should('contain.text', 'Your tasks');

    // Create a task via UI
    cy.get('input#title').type(`Test Task ${Date.now()}`);
    cy.get('input#url').type('dQw4w9WgXcQ');
    cy.get('.submit-form.bordered').find('input[type="submit"]').click();

    // Wait for task to appear and open it
    cy.get('.container-element img', { timeout: 10000 }).first().scrollIntoView();
    cy.get('.container-element img', { timeout: 10000 }).first().click({ force: true });

    // Wait for the todo list popup to appear and todo input to be visible
    cy.get('.todo-list', { timeout: 10000 }).should('be.visible');
    cy.get('input[placeholder="Add a new todo item"]', { timeout: 10000 }).should('exist');
  });

  after(function () {
    // Clean up by deleting the user from the database
    cy.request({
      method: 'DELETE',
      url: `http://localhost:${Cypress.env('REACT_APP_BACKEND_PORT') || 5000}/users/${uid}`
    });
  });

  it('R8UC1 - adds a todo item and keeps it after page refresh', () => {
    const description = `R8UC1 todo ${Date.now()}`

    cy.get('input[placeholder="Add a new todo item"]').type(description, { force: true });
    cy.contains('Add').click({ force: true });

    cy.get('.todo-list .todo-item').should('contain', description);

    cy.reload();

    // Re-login after reload since session is lost
    cy.get('input#email').type(email);
    cy.get('form').submit();
    cy.get('h1').should('contain.text', 'Your tasks');

    // Reopen the task to verify persistence
    cy.get('.container-element img', { timeout: 10000 }).first().scrollIntoView();
    cy.get('.container-element img', { timeout: 10000 }).first().click({ force: true });
    cy.get('.todo-list', { timeout: 10000 }).should('be.visible');

    cy.get('.todo-list .todo-item').should('contain', description);
  })

  it('R8UC2 - marks a todo item as completed and then uncompleted', () => {
    const description = `R8UC2 todo ${Date.now()}`

    cy.get('input[placeholder="Add a new todo item"]').type(description, { force: true });
    cy.contains('Add').click({ force: true });

    // Wait for the new item to appear
    cy.get('.todo-list .todo-item').contains(description).should('exist');
    cy.get('.todo-list .todo-item').contains(description).parent().as('todoItem');

    // Click the checker to mark complete
    cy.get('@todoItem').find('.checker').click({ force: true });
    cy.wait(300);  // Wait for state update
    cy.get('@todoItem').find('.checker').should('have.class', 'checked');

    // Click again to mark incomplete
    cy.get('@todoItem').find('.checker').click({ force: true });
    cy.wait(300);  // Wait for state update
    cy.get('@todoItem').find('.checker').should('not.have.class', 'checked');
  })

  it('R8UC3 - deletes a todo item and keeps it deleted after page refresh', () => {
    const description = `R8UC3 todo ${Date.now()}`;

    cy.get('input[placeholder="Add a new todo item"]').type(description, { force: true });
    cy.contains('Add').click({ force: true });

    // Wait for the new item to appear
    cy.contains('.todo-list .todo-item', description).should('exist');

    // Listen for the delete request
    cy.intercept(
      'DELETE',
      `http://localhost:${Cypress.env('REACT_APP_BACKEND_PORT') || 5000}/todos/byid/*`
    ).as('deleteTodo');

    // Delete the todo item
    cy.contains('.todo-list .todo-item', description)
      .find('span.remover')
      .click({ force: true });

    // Wait until backend has handled the delete
    cy.wait('@deleteTodo', { timeout: 5000 });

    // Verify it disappeared from the current popup
    cy.get('.todo-list').should('not.contain', description);

    // Refresh page to verify it stays deleted
    cy.reload();

    // Re-login after reload since session is lost
    cy.get('input#email').type(email);
    cy.get('form').submit();
    cy.get('h1').should('contain.text', 'Your tasks');

    // Reopen the task
    cy.get('.container-element img', { timeout: 10000 }).first().scrollIntoView();
    cy.get('.container-element img', { timeout: 10000 }).first().click({ force: true });
    cy.get('.todo-list', { timeout: 10000 }).should('be.visible');

    // Verify the deleted todo did not come back
    cy.get('.todo-list').should('not.contain', description);
  });
})