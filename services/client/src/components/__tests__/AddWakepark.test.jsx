import React from "react";
import { cleanup, fireEvent, wait } from "@testing-library/react";

import AddWakepark from "./../AddWakepark.jsx";
import localStorage from "./../../services/localStorage";

jest.mock("./../../services/localStorage", () => ({
  isPermitted: jest.fn(),
  getItem: jest.fn()
}));

// const onHandleAddWakepark = jest.fn();

afterEach(cleanup);

describe("renders", () => {
  localStorage.isPermitted.mockImplementation(() => false);

  // TODO: Test does not work properly...
  it("a redirect when post:wakeparks role is not present", () => {
    const { findByTestId } = renderWithRouter(<AddWakepark />);
    expect(findByTestId("redirect")).toBeTruthy();
  });
});

describe("renders", () => {
  localStorage.isPermitted.mockImplementation(() => true);

  it("properly", () => {
    const { getByText } = renderWithRouter(<AddWakepark />);
    expect(getByText("Add Wakepark")).toHaveClass("title");
    expect(localStorage.isPermitted).toHaveBeenCalled();
  });

  it("without values", () => {
    const { getByLabelText, getByText } = renderWithRouter(<AddWakepark />);

    const nameInput = getByLabelText("Name");
    expect(nameInput).toHaveAttribute("type", "text");
    expect(nameInput).not.toHaveValue();

    const descriptionInput = getByLabelText("Name");
    expect(descriptionInput).toHaveAttribute("type", "text");
    expect(descriptionInput).not.toHaveValue();

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
    const { getByLabelText, container, findByTestId } = renderWithRouter(
      <AddWakepark />
    );

    const form = container.querySelector("form");
    const nameInput = getByLabelText("Name");
    const descriptionInput = getByLabelText("Description");
    const latInput = getByLabelText("Latitude");
    const lngInput = getByLabelText("Longitude");
    const instaHandleInput = getByLabelText("Instagram Handle");

    fireEvent.blur(nameInput);
    fireEvent.blur(descriptionInput);
    fireEvent.blur(latInput);
    fireEvent.blur(lngInput);
    fireEvent.blur(instaHandleInput);

    expect((await findByTestId("errors-name")).innerHTML).toBe(
      "Please enter a name"
    );
    expect((await findByTestId("errors-description")).innerHTML).toBe(
      "Please enter a description"
    );
    expect((await findByTestId("errors-lat")).innerHTML).toBe(
      "Please enter a latitude"
    );
    expect((await findByTestId("errors-lng")).innerHTML).toBe(
      "Please enter a longitude"
    );

    fireEvent.submit(form);
  });

  it("when fields are valid", async () => {
    const { getByLabelText, container } = renderWithRouter(<AddWakepark />);

    const form = container.querySelector("form");
    const nameInput = getByLabelText("Name");
    const descriptionInput = getByLabelText("Description");
    const latInput = getByLabelText("Latitude");
    const lngInput = getByLabelText("Longitude");
    const instaHandleInput = getByLabelText("Instagram Handle");

    fireEvent.change(nameInput, { target: { value: "ImaginaryWakepark" } });
    fireEvent.blur(nameInput);
    fireEvent.change(descriptionInput, {
      target: { value: "This is an awesome wakepark!" }
    });
    fireEvent.blur(descriptionInput);
    fireEvent.change(latInput, { target: { value: "1.23" } });
    fireEvent.blur(latInput);
    fireEvent.change(lngInput, { target: { value: "4.56" } });
    fireEvent.blur(lngInput);
    fireEvent.change(instaHandleInput, {
      target: { value: "imaginary_wakepark" }
    });
    fireEvent.blur(instaHandleInput);

    fireEvent.submit(form);
  });
});
