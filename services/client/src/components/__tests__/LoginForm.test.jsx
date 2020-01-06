import React from "react";
import { cleanup, render } from "@testing-library/react";

import LoginForm from "./../LoginForm";

afterEach(cleanup);

describe("renders", () => {
  const props = {
    onHandleLoginFormSubmit: () => {
      return true;
    },
    isAuthenticated: () => {
      return false;
    }
  };

  it("properly", () => {
    const { getByText } = renderWithRouter(<LoginForm {...props} />);
    expect(getByText("Login")).toHaveClass("title");
  });

  it("with default props", () => {
    const { getByLabelText, getByText } = renderWithRouter(<LoginForm {...props} />);

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
    const { asFragment } = renderWithRouter(<LoginForm {...props} />);
    expect(asFragment()).toMatchSnapshot();
  });
});
