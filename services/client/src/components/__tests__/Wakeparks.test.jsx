import React from "react";
import { cleanup, wait } from "@testing-library/react";
import axios from "axios";

import Wakeparks from "./../Wakeparks";

afterEach(cleanup);

jest.mock("axios");

beforeEach(() => {
  axios.mockImplementation(() =>
    Promise.resolve({
      data: [
        {
          id: "1",
          name: "Stoke City Wakepark",
          description: "The only cable wakepark in Gauteng!",
          location: {
            lat: -25.952558,
            lng: 28.185543
          },
          social: {
            instagram: "https://www.instagram.com/stokecitywake"
          }
        }
      ]
    })
  );
});

it("renders a title", async () => {
  const { getByText } = renderWithRouter(<Wakeparks />);
  await wait(() => {
    expect(getByText("Wakeparks")).toHaveClass("title");
  });
});

it("renders a list of wakeparks", async () => {
  const { findByTestId } = renderWithRouter(<Wakeparks />);

  await wait(() => {
    expect(axios).toHaveBeenCalledTimes(2);
  });

  expect((await findByTestId("wakepark-name")).innerHTML).toBe("Stoke City Wakepark");
}, 6000);
