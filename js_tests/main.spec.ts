import { equal } from "assert";

import { setup } from "../js_src/main";

import { cleanDOM, loadDOMFromFile } from "./helpers";

describe("main", () => {
  before(async () => {
    await loadDOMFromFile("test.html");
  });

  describe("setup()", () => {
    it("can add 'django' API entry point to DOM window object", () => {
      setup(window);
      equal(typeof window.django, "object");
    });
  });

  after(async () => {
    await cleanDOM();
  });
});
