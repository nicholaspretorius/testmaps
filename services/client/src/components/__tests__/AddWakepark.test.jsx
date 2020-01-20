import React from "react";
import { cleanup } from "@testing-library/react";

import AddWakepark from "./../AddWakepark.jsx";

afterEach(cleanup);

describe("renders", () => {
  it("properly", () => {
    const { getByText } = renderWithRouter(<AddWakepark />);
    expect(getByText("Add Wakepark")).toHaveClass("title");
  });

  it("without values", () => {
    const { getByLabelText, getByText } = renderWithRouter(<AddWakepark />);

    const nameInput = getByLabelText("Name");
    expect(nameInput).toHaveAttribute("type", "text");
    expect(nameInput).not.toHaveValue();

    const latInput = getByLabelText("Latitude");
    expect(latInput).toHaveAttribute("type", "text");
    expect(latInput).not.toHaveValue();

    const lngInput = getByLabelText("Longitude");
    expect(lngInput).toHaveAttribute("type", "text");
    expect(lngInput).not.toHaveValue();

    const instaHandleInput = getByLabelText("Instagram Handle");
    expect(instaHandleInput).toHaveAttribute("type", "text");
    expect(instaHandleInput).not.toHaveValue();

    const buttonInput = getByText("Submit");
    expect(buttonInput).toHaveClass("button is-primary");
    expect(buttonInput).toHaveValue("Submit");
  });
});
