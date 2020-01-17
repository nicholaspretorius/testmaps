import React from "react";
import { cleanup } from "@testing-library/react";

import NotFound from "./../NotFound";

afterEach(cleanup);

it("renders properly", () => {
  const { getByTestId } = renderWithRouter(<NotFound />);
  expect(getByTestId("not-found").innerHTML).toBe("Unfortunately there is no page with that url.");
});
