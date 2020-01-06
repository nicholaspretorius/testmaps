import React from "react";
import { cleanup, render } from "@testing-library/react";

import RegisterForm from "./../RegisterForm";

afterEach(cleanup);

const props = {
  handleRegisterFormSubmit: () => {
    return true;
  }
};

it("renders properly", () => {
  const { getByText } = render(<RegisterForm {...props} />);
  expect(getByText("Register")).toHaveClass("title");
});

it("renders with default props", () => {
  const { getByLabelText, getByText } = render(<RegisterForm {...props} />);

  const emailInput = getByLabelText("Email");
  expect(emailInput).toHaveAttribute("type", "email");
  expect(emailInput).not.toHaveValue();

  const passwordInput = getByLabelText("Password");
  expect(passwordInput).toHaveAttribute("type", "password");
  expect(passwordInput).not.toHaveValue();

  const buttonInput = getByText("Submit");
  expect(buttonInput).toHaveValue("Submit");
});

it("renders", () => {
  const { asFragment } = renderWithRouter(<RegisterForm {...props} />);
  expect(asFragment()).toMatchSnapshot();
});
