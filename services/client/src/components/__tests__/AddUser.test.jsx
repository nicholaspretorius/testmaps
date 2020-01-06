import React from "react";
import { render, cleanup } from "@testing-library/react";

import AddUser from "./../AddUser";

afterEach(cleanup);

describe("renders", () => {
  const props = {
    addUser: () => true
  };

  it("with default props", () => {
    const { getByLabelText, getByText } = render(<AddUser {...props} />);

    const emailInput = getByLabelText("Email");
    expect(emailInput).toHaveAttribute("type", "email");
    expect(emailInput).not.toHaveValue();

    const passwordInput = getByLabelText("Password");
    expect(passwordInput).toHaveAttribute("type", "password");
    expect(passwordInput).not.toHaveValue();

    const buttonInput = getByText("Submit");
    expect(buttonInput).toHaveValue("Submit");
  });

  it("a snapshot", () => {
    const { asFragment } = render(<AddUser {...props} />);
    expect(asFragment()).toMatchSnapshot();
  });
});
