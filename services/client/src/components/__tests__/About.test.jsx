import React from "react";
import { render, cleanup } from "@testing-library/react";

import About from "./../About";

afterEach(cleanup);

it("renders properly", () => {
  const { getByText } = render(<About />);
  expect(getByText("About us content goes here.")).toHaveClass("content");
});

it("renders", () => {
  const { asFragment } = render(<About />);
  expect(asFragment()).toMatchSnapshot();
});
