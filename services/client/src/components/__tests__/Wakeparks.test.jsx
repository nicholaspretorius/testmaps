import React from "react";
import { render, cleanup } from "@testing-library/react";

import Wakeparks from "./../Wakeparks";

afterEach(cleanup);

it("renders a title", () => {
  const { getByText } = render(<Wakeparks />);
  expect(getByText("Wakeparks")).toHaveClass("title");
});
