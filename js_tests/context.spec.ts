import { equal } from "assert";

import { getContext } from "../js_src/context";

import { cleanDOM, loadDOMFromFile } from "./helpers";

describe("Test context module", () => {
  before(async () => {
    await loadDOMFromFile("test.html");
  });
  it("getContext() can parse the JSON script tag generated by Django", () => {
    const data = getContext();
    equal(data.myString, "this is a string");
  });
  after(async () => {
    await cleanDOM();
  });
});