import { equal } from "assert";
import { JSDOM } from "jsdom"
import { setup } from "../js_src/main";

const { window } = new JSDOM('<!doctype html><html><body></body></html>') as unknown as Window;

describe("Test main module", () => {
  it("setup() can add 'django' API entry point to DOM window object", () => {
    setup(window);
    equal(typeof window.django, "object");
  });
});
