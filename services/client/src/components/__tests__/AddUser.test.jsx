import React from "react";
import { render, cleanup } from "@testing-library/react";

import AddUser from "./../AddUser";

afterEach(cleanup);

it("renders with default props", () => {
  const { getByLabelText, getByText } = render(<AddUser email="" handleChange={() => true} />);

  const emailInput = getByLabelText("Email");
  expect(emailInput).toHaveAttribute("type", "email");
  expect(emailInput).toHaveAttribute("required");
  expect(emailInput).not.toHaveValue();

  const buttonInput = getByText("Submit");
  expect(buttonInput).toHaveValue("Submit");
});

it("renders", () => {
  const { asFragment } = render(<AddUser email="" handleChange={() => true} />);
  expect(asFragment()).toMatchSnapshot();
});
