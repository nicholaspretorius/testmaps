xdescribe("About Page", () => {
  beforeEach(() => {
    cy.viewport(1200, 900);
  });

  it("visits the about page", () => {
    cy.visit("/about");
  });

  it("displays the title", () => {
    cy.get("h3.title").contains("About");
  });

  it("displays the introductory paragraph", () => {
    cy.get("p.content").contains("Wakemaps is a wakepark listing directory.");
  });
});
