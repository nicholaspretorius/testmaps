import React from "react";
import { cleanup, wait } from "@testing-library/react";

import Callback from "./../Callback";
import localStorage from "../../services/localStorage";

afterEach(cleanup);

localStorage.setItem = jest.fn();

const props = {
  onHandleAuth: () => {
    return true;
  }
};

it("should render", () => {
  const { getByText } = renderWithRouter(<Callback {...props} />);
  expect(getByText("Loading profile...")).toBeVisible();
});

xit("should set accessToken in localStorage", async () => {
  await wait(() => {
    expect(localStorage.setItem).toBeCalledWith("accessToken");
  });
});
