import { equal } from "assert";
import { JSDOM } from "jsdom"

import { loadText } from "./helpers";
import { setup } from "../js_src/main";

const { window } = new JSDOM(loadText("test.html")) as unknown as Window;

describe("Test main module", () => {
  it("setup() can add 'django' API entry point to DOM window object", () => {
    setup(window);
    equal(typeof window.django, "object");
  });
});
