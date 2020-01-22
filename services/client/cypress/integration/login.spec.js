describe("login", () => {
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
});
