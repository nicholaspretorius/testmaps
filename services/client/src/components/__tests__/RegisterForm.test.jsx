import React from "react";
import { cleanup, fireEvent } from "@testing-library/react";

import RegisterForm from "./../RegisterForm";

afterEach(cleanup);

describe("renders", () => {
  const props = {
    onHandleRegisterFormSubmit: () => {
      return true;
    },
    isAuthenticated: () => {
      return false;
    }
  };

  it("properly", () => {
    const { getByText } = renderWithRouter(<RegisterForm {...props} />);
    expect(getByText("Register")).toHaveClass("title");
  });

  it("with default props", () => {
    const { getByLabelText, getByText } = renderWithRouter(<RegisterForm {...props} />);

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
    const { asFragment } = renderWithRouter(<RegisterForm {...props} />);
    expect(asFragment()).toMatchSnapshot();
  });
});

describe("handles form validation correctly", () => {
  const mockProps = {
    onHandleRegisterFormSubmit: jest.fn(),
    isAuthenticated: jest.fn()
  };

  it("when fields are empty", async () => {});
  it("when email field is not valid", async () => {});
  it("when fields are not the correct length", async () => {});
  it("when fields are valid", async () => {});
});
