import React from "react";
import { cleanup, wait } from "@testing-library/react";

import NavBar from "./../NavBar";

afterEach(cleanup);

describe("when not authenticated", () => {
  const props = {
    title: "Hello, world!",
    logoutUser: () => {
      return true;
    },
    isAuthenticated: jest.fn().mockImplementation(() => false)
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
      expect(props.isAuthenticated).toHaveBeenCalledTimes(2);
    });
    expect((await findByTestId("nav-about")).innerHTML).toBe("About");
    expect((await findByTestId("nav-register")).innerHTML).toBe("Register");
    expect((await findByTestId("nav-login")).innerHTML).toBe("Login");
  });

  it("renders", () => {
    const { asFragment } = renderWithRouter(<NavBar {...props} />);
    expect(asFragment()).toMatchSnapshot();
  });
});

describe("when authenticated", () => {
  const props = {
    title: "Hello, world!",
    logoutUser: () => {
      return false;
    },
    isAuthenticated: jest.fn().mockImplementation(() => true)
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
      expect(props.isAuthenticated).toHaveBeenCalledTimes(2);
    });
    expect((await findByTestId("nav-about")).innerHTML).toBe("About");
    expect((await findByTestId("nav-status")).innerHTML).toBe("User Status");
    expect((await findByTestId("nav-logout")).innerHTML).toBe("Logout");
  });

  it("renders", () => {
    const { asFragment } = renderWithRouter(<NavBar {...props} />);
    expect(asFragment()).toMatchSnapshot();
  });
});
