import { equal } from "assert";

import { setup } from "../js_src/main";

import { cleanDOM, loadDOMFromFile } from "./helpers";

interface TestURL {
  readonly name: string;
  readonly kwargs: { [key: string]: number | string };
  readonly expected_url: string;
}

describe("Test urls module: reverse func", () => {
  const testURLs: TestURL[] = [
    { name: "fake:page", kwargs: { num: "5" }, expected_url: "/page/5" }
  ];

  before(async () => {
    await loadDOMFromFile("test.html");
    setup(window);
  });

  testURLs.forEach((params: TestURL) => {
    it(`reverse() can successfully reverse URL '${params.name}'`, () => {
      const url = window.django.reverse(params.name, params.kwargs);
      equal(url, params.expected_url);
    });
  });

  after(async () => {
    await cleanDOM();
  });
});
