import React from "react";
import { cleanup, wait } from "@testing-library/react";

import NavBar from "./../NavBar";

afterEach(cleanup);

describe("when not authenticated", () => {
  const props = {
    title: "Hello, world!",
    isAuth: jest.fn().mockImplementation(() => false),
    profile: null,
    signIn: () => true,
    signOut: () => false
  };

  it("renders a title", () => {
    const { getByText } = renderWithRouter(<NavBar {...props} />);
    expect(getByText(props.title)).toHaveClass("nav-title");
  });

  it("renders the default props", async () => {
    const { getByText, findByTestId } = renderWithRouter(<NavBar {...props} />);
    expect(getByText(props.title)).toHaveClass("nav-title");
    await wait(() => {
      // TODO: Investigate why it is running twice... render/componentDidMount
      expect(props.isAuth).toHaveBeenCalledTimes(6);
    });
    expect((await findByTestId("nav-about")).innerHTML).toBe("About");
    expect((await findByTestId("nav-signin")).innerHTML).toBe("SignIn");
    // expect((await findByTestId("nav-login")).innerHTML).toBe("Login");
  });

  it("renders", () => {
    const { asFragment } = renderWithRouter(<NavBar {...props} />);
    expect(asFragment()).toMatchSnapshot();
  });
});

describe("when authenticated", () => {
  const props = {
    title: "Hello, world!",
    isAuth: jest.fn().mockImplementation(() => true),
    profile: { name: "test@test.com" },
    signIn: () => false,
    signOut: () => true
  };

  it("renders a title", () => {
    const { getByText } = renderWithRouter(<NavBar {...props} />);
    expect(getByText(props.title)).toHaveClass("nav-title");
  });

  it("renders the default props", async () => {
    const { getByText, findByTestId } = renderWithRouter(<NavBar {...props} />);
    expect(getByText(props.title)).toHaveClass("nav-title");
    await wait(() => {
      // TODO: Investigate why it is running twice... render/componentDidMount
      expect(props.isAuth).toHaveBeenCalledTimes(6);
    });
    expect((await findByTestId("nav-about")).innerHTML).toBe("About");
    expect((await findByTestId("nav-signout")).innerHTML).toBe("SignOut");
    expect((await findByTestId("nav-sanity")).innerHTML).toBe("Sanity");
  });

  it("renders", () => {
    const { asFragment } = renderWithRouter(<NavBar {...props} />);
    expect(asFragment()).toMatchSnapshot();
  });
});
