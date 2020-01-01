import React from "react";
import { render, cleanup } from "@testing-library/react";

import Users from "./../Users";

afterEach(cleanup);

const users = [
  {
    id: 1,
    email: "test1@test.com"
  },
  {
    id: 2,
    email: "test2@test.com"
  }
];

it("renders an email", () => {
  const { getByText } = render(<Users users={users} />);
  expect(getByText("test1@test.com")).toHaveClass("user-email");
  expect(getByText("test2@test.com")).toHaveClass("user-email");
});
