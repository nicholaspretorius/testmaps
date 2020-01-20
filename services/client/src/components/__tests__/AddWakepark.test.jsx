import React from "react";
import { cleanup, fireEvent } from "@testing-library/react";

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

  it("a snapshot", () => {
    const { asFragment } = renderWithRouter(<AddWakepark />);
    expect(asFragment()).toMatchSnapshot();
  });
});

describe("handles form validation correctly", () => {
  it("when fields are empty", async () => {
    const { getByLabelText, container, findByTestId } = renderWithRouter(<AddWakepark />);

    const form = container.querySelector("form");
    const nameInput = getByLabelText("Name");
    const latInput = getByLabelText("Latitude");
    const lngInput = getByLabelText("Longitude");
    const instaHandleInput = getByLabelText("Instagram Handle");

    fireEvent.blur(nameInput);
    fireEvent.blur(latInput);
    fireEvent.blur(lngInput);
    fireEvent.blur(instaHandleInput);

    expect((await findByTestId("errors-name")).innerHTML).toBe("Please enter a name");
    expect((await findByTestId("errors-lat")).innerHTML).toBe("Please enter a latitude");
    expect((await findByTestId("errors-lng")).innerHTML).toBe("Please enter a longitude");

    fireEvent.submit(form);
  });
});
