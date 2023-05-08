import { equal, throws } from "assert";

import { setup } from "../js_src/main";

import { cleanDOM, loadDOMFromFile } from "./helpers";

interface TestURL {
  readonly name: string;
  readonly kwargs: { [key: string]: number | string };
  readonly expected_url: string;
}

describe("urls", () => {
  before(async () => {
    await loadDOMFromFile("test.html");
    setup(window);
  });

  describe("reverse()", () => {
    // defined in test_project/fake/urls.py
    const testURLs: TestURL[] = [
      { name: "fake:test", kwargs: {}, expected_url: "/" },
      { name: "fake:page", kwargs: { num: "5" }, expected_url: "/page/5" },
      {
        name: "fake:named_page",
        kwargs: { slug: "my-page", num: 4 },
        expected_url: "/my-page/4"
      }
    ];

    testURLs.forEach((params: TestURL) => {
      it(`can successfully reverse URL '${params.name}'`, () => {
        const url = window.django.reverse(params.name, params.kwargs);
        equal(url, params.expected_url);
      });
    });

    it("throws NoReverseMatch with valid pathName but invalid kwarg type", () => {
      throws(
        () => {
          window.django.reverse("fake:page", { num: "string" });
        },
        { name: "NoReverseMatch" }
      );
    });

    it("throws NoReverseMatch with invalid pathName", () => {
      throws(
        () => {
          window.django.reverse("missing:path");
        },
        { name: "NoReverseMatch" }
      );
    });
  });

  describe("converters.register() + reverse()", () => {
    it("can register a custom converter and successfully reverse URL", () => {
      const fourDigitYearConverter = new window.django.urls.Converter("yyyy", /[0-9]{4}/);
      window.django.urls.converters.register(fourDigitYearConverter);

      const url = window.django.reverse("fake:custom_converter", { year: 2005 });
      equal(url, "/articles/2005");
    });
  });

  after(async () => {
    await cleanDOM();
  });
});
