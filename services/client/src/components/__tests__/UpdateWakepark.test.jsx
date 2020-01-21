import React from "react";
import { cleanup, wait, waitForElement } from "@testing-library/react";
import axios from "axios";

import UpdateWakepark from "./../UpdateWakepark";
import localStorage from "./../../services/localStorage";

jest.mock("axios");

jest.mock("./../../services/localStorage", () => ({
  isPermitted: jest.fn(),
  getItem: jest.fn()
}));

axios.mockImplementation(() =>
  Promise.resolve({
    data: {
      id: 1,
      name: "Wakepark",
      description: "Description goes here",
      location: {
        lat: 1.23,
        lng: 4.56
      },
      social: {
        instagram: "https://www.instagram.com/wakepark"
      }
    }
  })
);

const mockProps = {
  match: {
    params: { id: 1 },
    isExact: true,
    path: "",
    url: ""
  }
};

afterEach(cleanup);

xdescribe("renders", () => {
  // TODO: Test does not work properly...
  it("a redirect when post:wakeparks role is not present", () => {
    localStorage.isPermitted.mockImplementation(() => false);
    const { findByTestId } = renderWithRouter(
      <UpdateWakepark {...mockProps} />
    );
    expect(findByTestId("redirect")).toBeTruthy();
  });
});

describe("renders", () => {
  it("properly", async () => {
    localStorage.isPermitted.mockImplementation(() => true);
    const { getByText } = renderWithRouter(<UpdateWakepark {...mockProps} />);
    expect(getByText("Update Wakepark")).toHaveClass("title");
    expect(localStorage.isPermitted).toHaveBeenCalled();

    await wait(() => {
      expect(axios).toHaveBeenCalledTimes(1);
    });
  });

  it("with wakepark values", async () => {
    const { getByLabelText, getByText } = renderWithRouter(
      <UpdateWakepark {...mockProps} />
    );

    const nameInput = await waitForElement(() => getByLabelText("Name"));
    expect(nameInput).toHaveAttribute("type", "text");
    expect(nameInput).toHaveValue("Wakepark");

    const descriptionInput = getByLabelText("Description");
    expect(descriptionInput).toHaveAttribute("type", "text");
    expect(descriptionInput).toHaveValue("Description goes here");

    const latInput = getByLabelText("Latitude");
    expect(latInput).toHaveAttribute("type", "text");
    expect(latInput).toHaveValue("1.23");

    const lngInput = getByLabelText("Longitude");
    expect(lngInput).toHaveAttribute("type", "text");
    expect(lngInput).toHaveValue("4.56");

    const instaHandleInput = getByLabelText("Instagram Handle");
    expect(instaHandleInput).toHaveAttribute("type", "text");
    expect(instaHandleInput).toHaveValue("wakepark");

    const buttonInput = getByText("Submit");
    expect(buttonInput).toHaveClass("button is-primary");
    expect(buttonInput).toHaveValue("Submit");
  });
});
