describe("profile page", () => {
  beforeEach(() => {
    cy.viewport(1200, 900);
  });

  const baseUrl = Cypress.config().baseUrl;

  // logged out
  describe("when logged out", () => {
    it("visits the page and displays 404 page", () => {
      cy.visit("/profile")
        .url()
        .should("eq", baseUrl + "/profile");

      cy.get("h3.title").contains("404 Not Found.");

      cy.get("[data-testid=not-found]").contains("Unfortunately there is no page with that url.");
    });
  });

  // regular user
  describe("when logged in as regular user", () => {
    const user = Cypress.env("auth_user_username");
    const pass = Cypress.env("auth_user_password");

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

    it("displays the profile page", () => {
      cy.get("[data-testid=nav-profile]")
        .click()
        .url()
        .should("include", "/profile");
    });

    it("displays the title", () => {
      cy.get("h3.title").contains("Profile");
    });

    it("displays the name, email and sub", () => {
      cy.get("div.user-profile>ul>li")
        .eq(0)
        .contains("Name: ");
      cy.get("div.user-profile>ul>li")
        .eq(1)
        .contains("Email: ");
      cy.get("div.user-profile>ul>li")
        .eq(2)
        .contains("Sub: ");
    });

    it("displays the accessToken", () => {
      cy.get("[data-testid=access-token]");
    });

    it("displays the permissions", () => {
      cy.get("[data-testid=permissions]");
    });

    it("logs the user out", () => {
      cy.get("[data-testid=nav-signout]")
        .click()
        .url()
        .should("eq", Cypress.config().baseUrl + "/");
    });
  });
});
