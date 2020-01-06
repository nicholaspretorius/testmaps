import React from "react";
import { cleanup, render } from "@testing-library/react";

import RegisterForm from "./../RegisterForm";

afterEach(cleanup);

it("renders properly", () => {
  const { getByText } = render(<RegisterForm />);
  expect(getByText("Register")).toHaveClass("title");
});

it("renders", () => {
  const { asFragment } = renderWithRouter(<RegisterForm />);
  expect(asFragment()).toMatchSnapshot();
});
