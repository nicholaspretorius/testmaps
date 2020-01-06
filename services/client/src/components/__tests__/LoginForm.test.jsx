import React from "react";
import { cleanup, render } from "@testing-library/react";

import LoginForm from "./../LoginForm";

afterEach(cleanup);

it("renders properly", () => {
  const { getByText } = render(<LoginForm />);
  expect(getByText("Login")).toHaveClass("title");
});

it("renders", () => {
  const { asFragment } = renderWithRouter(<LoginForm />);
  expect(asFragment()).toMatchSnapshot();
});
