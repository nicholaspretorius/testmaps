describe("login", () => {
  beforeEach(() => {
    cy.viewport(1200, 900);
  });

  it("should login successfully", () => {
    cy.login()
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
    const testEmail = "e2e-testing@madeupdomainname.com";

    cy.get("[data-testid=nav-profile]")
      .contains(testEmail)
      .should("have.attr", "href")
      .and("include", "profile");
  });

  it("displays the navbar logout link correctly", () => {
    cy.get("[data-testid=nav-signout]").contains("Logout");
  });
});
