import React from "react";
import { cleanup, wait } from "@testing-library/react";
import axios from "axios";

import SanityCheck from "./../SanityCheck";

afterEach(cleanup);

jest.mock("axios");

axios.mockImplementationOnce(() =>
  Promise.resolve({
    data: {
      status: "success",
      hello: "Riders!"
    }
  })
);

describe("renders", () => {
  it("properly when authenticated", async () => {
    const { findByTestId } = renderWithRouter(<SanityCheck />);

    await wait(() => {
      expect(axios).toHaveBeenCalledTimes(1);
    });

    expect((await findByTestId("message")).innerHTML).toBe("Riders!");
  });
});
