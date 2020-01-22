describe("App", () => {
  it("loads", () => {
    cy.visit("/");
    cy.get("h3").contains("Wakeparks");
  });
});
