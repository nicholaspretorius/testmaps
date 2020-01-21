import React from "react";
import { cleanup } from "@testing-library/react";

import Callback from "./../Callback";

afterEach(cleanup);

jest.mock("../../services/localStorage", () => ({
  setItem: jest.fn()
}));

const props = {
  onHandleAuth: jest.fn()
};

it("should render", () => {
  const { getByText } = renderWithRouter(<Callback {...props} />);
  expect(getByText("Loading profile...")).toBeVisible();
  expect(props.onHandleAuth).toHaveBeenCalledTimes(1);
});
