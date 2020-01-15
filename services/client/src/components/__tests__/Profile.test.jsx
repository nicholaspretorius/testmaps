import React from "react";
import { cleanup, render } from "@testing-library/react";

import Profile from "./../Profile";
// import localStorage from "../../services/localStorage";

afterEach(cleanup);

// localStorage.mockImplementationOnce(() => {
//   return "eyJhbGciOiJSUzI1NiIsInR5c";
// });

const props = {
  profile: {
    name: "Joe Soap",
    email: "joe@soap.com",
    sub: "auth0|k0upeznaul5tvi1yfjmw714d"
  }
};

localStorage = {
  getItem: () => "eyJhbGciOiJSUzI1NiIsInR5c"
};

// const localStorage = {
//   getItem: jest.fn()
// };

// localStorage.getItem.mockReturnValue(global.localStorage.getItem("accessToken"));

it("renders a title", () => {
  const { getByText } = renderWithRouter(<Profile {...props} />);
  expect(getByText("Profile")).toHaveClass("title");
});

it("renders an access token", () => {
  const { getByTestId } = renderWithRouter(<Profile {...props} />);
  expect(getByTestId("access-token")).toBeVisible();
  // expect(getByTestId("access-token").innerHTML).toBe("eyJhbGciOiJSUzI1NiIsInR5c");
});

it("renders a name, email and sub", () => {
  const { getByTestId } = renderWithRouter(<Profile {...props} />);
  expect(getByTestId("user-name").innerHTML).toBe("Joe Soap");
  expect(getByTestId("user-email").innerHTML).toBe("joe@soap.com");
  expect(getByTestId("user-sub").innerHTML).toContain("auth0|");
});
