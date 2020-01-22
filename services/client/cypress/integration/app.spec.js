describe("App Home Page", () => {
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
