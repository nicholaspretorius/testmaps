describe("App Home Page: Logged Out", () => {
  context("MacBoook Pro 15", () => {
    beforeEach(() => {
      cy.viewport(1200, 900);
    });

    it("visits the page", () => {
      cy.visit("/");
    });

    it("displays the page title", () => {
      cy.visit("/")
        .get("h3")
        .contains("Wakeparks");
    });

    it("displays the logged out navbar view", () => {
      cy.visit("/")
        .get("a.nav-title")
        .contains("Wakemaps")
        .get("a.navbar-item")
        .contains("About")
        .get("span.navbar-item")
        .contains("Login");
    });
  });
});

describe("App Home Page: Logged in", () => {
  const baseUrl = Cypress.config().baseUrl;

  beforeEach(() => {
    cy.viewport(1200, 900);
  });

  describe("as a regular user", () => {
    const user = Cypress.env("auth_user_username");
    const pass = Cypress.env("auth_user_password");

    it("should login regular user successfully", () => {
      cy.login(user, pass)
        .then(res => {
          return res.body;
        })
        .then(data => {
          const { access_token, expires_in, id_token } = data;

          const auth0State = {
            nonce: "",
            state: "test-state"
          };

          const callbackUrl = `/callback#access_token=${access_token}&scope=openid&id_token=${id_token}&expires_in=${expires_in}&token_type=Bearer&state=${auth0State.state}`;

          cy.visit(callbackUrl, {
            onBeforeLoad(win) {
              win.document.cookie = "com.auth0.auth.test-state=" + JSON.stringify(auth0State);
            }
          });
        });
    });

    it("does not display an 'Add Wakepark' button", () => {
      cy.get("[data-testid=add-wakepark]").should("not.be.visible");
    });

    it("logs the regular user out", () => {
      cy.get("[data-testid=nav-signout]")
        .click()
        .url()
        .should("eq", baseUrl + "/");
    });
  });

  describe("as a parkadmin user", () => {
    const user = Cypress.env("auth_parkadmin_username");
    const pass = Cypress.env("auth_parkadmin_password");

    it("should login the parkadmin user successfully", () => {
      cy.login(user, pass)
        .then(res => {
          return res.body;
        })
        .then(data => {
          const { access_token, expires_in, id_token } = data;

          const auth0State = {
            nonce: "",
            state: "test-state"
          };

          const callbackUrl = `/callback#access_token=${access_token}&scope=openid&id_token=${id_token}&expires_in=${expires_in}&token_type=Bearer&state=${auth0State.state}`;

          cy.visit(callbackUrl, {
            onBeforeLoad(win) {
              win.document.cookie = "com.auth0.auth.test-state=" + JSON.stringify(auth0State);
            }
          });
        });
    });

    it("displays an 'Add Wakepark' button", () => {
      cy.get("[data-testid=add-wakepark]")
        .should("be.visible")
        .contains("Add Wakepark")
        .and("have.attr", "href")
        .and("include", "/add-wakepark");
    });

    // it("clicks on the 'AddWakepark' button", () => {
    //   cy.get("[data-testid=add-wakepark]")
    //     .should("be.visible")
    //     .contains("Add Wakepark")
    //     .and("have.attr", "href")
    //     .and("include", "/add-wakepark");

    //   cy.get("[data-testid=add-wakepark]")
    //     .click()
    //     .url()
    //     .should("eq", baseUrl + "/add-wakepark");
    // });

    // it("should have a title", () => {
    //   cy.get("h3.title").contains("Add Wakepark");
    // });

    // it("displays the 'Name' input field", () => {
    //   cy.get('label[for="input-name"]')
    //     .contains("Name")
    //     .should("have.attr", "for")
    //     .and("include", "input-name");

    //   cy.get("input#input-name")
    //     .should("have.value", "")
    //     .invoke("attr", "placeholder")
    //     .should("contain", "Enter the wakepark name");
    // });

    // it("displays the 'Description' input field", () => {
    //   cy.get('label[for="input-description"]')
    //     .contains("Description")
    //     .should("have.attr", "for")
    //     .and("include", "input-description");

    //   cy.get("input#input-description")
    //     .should("have.value", "")
    //     .invoke("attr", "placeholder")
    //     .should("contain", "Enter the wakepark description");
    // });

    // it("displays the 'Latitude' input field", () => {
    //   cy.get('label[for="input-latitude"]')
    //     .contains("Latitude")
    //     .should("have.attr", "for")
    //     .and("include", "input-latitude");

    //   cy.get("input#input-latitude")
    //     .should("have.value", "")
    //     .invoke("attr", "placeholder")
    //     .should("contain", "Enter the wakepark latitude location");
    // });

    // it("displays the 'Longitude' input field", () => {
    //   cy.get('label[for="input-longitude"]')
    //     .contains("Longitude")
    //     .should("have.attr", "for")
    //     .and("include", "input-longitude");

    //   cy.get("input#input-longitude")
    //     .should("have.value", "")
    //     .invoke("attr", "placeholder")
    //     .should("contain", "Enter the wakepark longitude location");
    // });

    // it("displays the 'Instagram Handle' input field", () => {
    //   cy.get('label[for="input-instagram-handle"]')
    //     .contains("Instagram Handle")
    //     .should("have.attr", "for")
    //     .and("include", "input-instagram-handle");

    //   cy.get("input#input-instagram-handle")
    //     .should("have.value", "")
    //     .invoke("attr", "placeholder")
    //     .should("contain", "Enter the wakepark Instagram handle");
    // });

    // it("displays the 'Submit' button", () => {
    //   cy.get("input[type='submit']")
    //     .contains("Submit")
    //     .should("have.class", "button is-primary");
    // });

    it("logs the user out", () => {
      cy.get("[data-testid=nav-signout]")
        .click()
        .url()
        .should("eq", baseUrl + "/");
    });
  });
});
