import React from "react";
import { cleanup, wait } from "@testing-library/react";
import axios from "axios";

import SanityCheck from "./../SanityCheck";
import auth from "./../../services/auth";

afterEach(cleanup);

jest.mock("axios");
jest.mock("./../../services/auth");

axios.mockImplementationOnce(() =>
  Promise.resolve({
    data: {
      status: "success",
      hello: "Riders!"
    }
  })
);

const email = "test@test.com";

auth.getProfile.mockImplementationOnce(() => {
  Promise.resolve({
    data: {
      email
    }
  });
});

describe("renders", () => {
  it("properly when authenticated", async () => {
    const { findByTestId } = renderWithRouter(<SanityCheck />);

    await wait(() => {
      expect(axios).toHaveBeenCalledTimes(1);
    });

    expect(auth.getProfile).toHaveBeenCalledTimes(1);

    expect((await findByTestId("message")).innerHTML).toBe("Riders!");
    expect((await findByTestId("email")).innerHTML).toBe(email);
  });
});
