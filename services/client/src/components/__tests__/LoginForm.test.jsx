import React from "react";
import { cleanup, fireEvent, wait } from "@testing-library/react";

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
    const { getByLabelText, getByText } = renderWithRouter(
      <LoginForm {...props} />
    );

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

describe("handles form validation correctly", () => {
  const mockProps = {
    onHandleLoginFormSubmit: jest.fn(),
    isAuthenticated: jest.fn()
  };

  it("when fields are empty", async () => {
    const { getByLabelText, container, findByTestId } = renderWithRouter(
      <LoginForm {...mockProps} />
    );

    const form = container.querySelector("form");
    const emailInput = getByLabelText("Email");
    const passwordInput = getByLabelText("Password");

    expect(mockProps.onHandleLoginFormSubmit).toHaveBeenCalledTimes(0);

    fireEvent.blur(emailInput);
    fireEvent.blur(passwordInput);

    expect((await findByTestId("errors-email")).innerHTML).toBe(
      "Email is required."
    );
    expect((await findByTestId("errors-password")).innerHTML).toBe(
      "Password is required."
    );

    fireEvent.submit(form);

    await wait(() => {
      expect(mockProps.onHandleLoginFormSubmit).toHaveBeenCalledTimes(0);
    });
  });

  it("when email field is not valid", async () => {
    const { getByLabelText, container, findByTestId } = renderWithRouter(
      <LoginForm {...mockProps} />
    );

    const form = container.querySelector("form");
    const emailInput = getByLabelText("Email");

    expect(mockProps.onHandleLoginFormSubmit).toHaveBeenCalledTimes(0);

    fireEvent.change(emailInput, { target: { value: "invalid" } });
    fireEvent.blur(emailInput);

    expect((await findByTestId("errors-email")).innerHTML).toBe(
      "Please enter a valid email."
    );

    fireEvent.submit(form);

    await wait(() => {
      expect(mockProps.onHandleLoginFormSubmit).toHaveBeenCalledTimes(0);
    });
  });

  it("when fields are not the correct length", async () => {
    const { getByLabelText, container, findByTestId } = renderWithRouter(
      <LoginForm {...mockProps} />
    );

    const form = container.querySelector("form");
    const emailInput = getByLabelText("Email");
    const passwordInput = getByLabelText("Password");

    expect(mockProps.onHandleLoginFormSubmit).toHaveBeenCalledTimes(0);

    fireEvent.change(emailInput, { target: { value: "a@b.c" } });
    fireEvent.blur(emailInput);
    fireEvent.change(passwordInput, { target: { value: "short" } });
    fireEvent.blur(passwordInput);

    expect((await findByTestId("errors-email")).innerHTML).toBe(
      "Email must be 6 or more characters."
    );
    expect((await findByTestId("errors-password")).innerHTML).toBe(
      "Password must be 8 or more characters."
    );

    fireEvent.submit(form);

    await wait(() => {
      expect(mockProps.onHandleLoginFormSubmit).toHaveBeenCalledTimes(0);
    });
  });

  it("when fields are valid", async () => {
    const { getByLabelText, container } = renderWithRouter(
      <LoginForm {...mockProps} />
    );

    const form = container.querySelector("form");
    const emailInput = getByLabelText("Email");
    const passwordInput = getByLabelText("Password");

    expect(mockProps.onHandleLoginFormSubmit).toHaveBeenCalledTimes(0);

    fireEvent.change(emailInput, { target: { value: "test@test.com" } });
    fireEvent.blur(emailInput);
    fireEvent.change(passwordInput, { target: { value: "password" } });
    fireEvent.blur(passwordInput);

    fireEvent.submit(form);

    await wait(() => {
      expect(mockProps.onHandleLoginFormSubmit).toHaveBeenCalledTimes(1);
    });
  });
});
