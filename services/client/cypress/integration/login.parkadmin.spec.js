describe("login parkadmin user", () => {
  beforeEach(() => {
    cy.viewport(1200, 900);
  });

  const user = Cypress.env("auth_parkadmin_username");
  const pass = Cypress.env("auth_parkadmin_password");

  it("should login successfully", () => {
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

  it("displays the navbar profile link correctly", () => {
    cy.get("[data-testid=nav-profile]")
      .contains(user)
      .should("have.attr", "href")
      .and("include", "profile");
  });

  it("displays the navbar logout link correctly", () => {
    cy.get("[data-testid=nav-signout]").contains("Logout");
  });

  it("logs the user out", () => {
    cy.get("[data-testid=nav-signout]")
      .click()
      .url()
      .should("eq", Cypress.config().baseUrl + "/");
  });
});
