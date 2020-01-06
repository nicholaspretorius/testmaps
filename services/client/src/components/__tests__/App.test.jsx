import React from "react";
import { cleanup } from "@testing-library/react";

import App from "./../App";

afterEach(cleanup);

it("renders a snapshot", () => {
  const { asFragment } = renderWithRouter(<App />);
  expect(asFragment()).toMatchSnapshot();
});
