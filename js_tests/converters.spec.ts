import { equal, throws } from "assert";

import { Converter, Converters } from "../js_src/converters";

describe("converters", () => {
  const converters = new Converters();

  describe("Converter", () => {
    it("throws TypeError when passed global regex", () => {
      throws(
        () => {
          new Converter("test", /.*/g);
        },
        { name: "TypeError" }
      );
    });
  });

  describe("defaultConverters", () => {
    interface TestValue {
      name: string;
      valid: number | string;
      invalid: number | string | null;
    }

    const testValues: TestValue[] = [
      { name: "int", valid: 5, invalid: "x5" },
      { name: "path", valid: "page", invalid: null },
      { name: "slug", valid: "this-is-a-slug", invalid: "@not-a-slug" },
      { name: "str", valid: "string", invalid: "not-a-string/" },
      { name: "uuid", valid: "e7fd7d45-b0dd-4cab-b31a-3a3b6f03b812", invalid: "5" }
    ];

    testValues.forEach(({ name, valid, invalid }) => {
      it(`is idempotent when performing validation ('${name}')`, () => {
        const converter = converters.get(name);
        equal(converter.check(valid), true);
        equal(converter.check(valid), true);
        if (invalid !== null) {
          equal(converter.check(invalid), false);
          equal(converter.check(invalid), false);
        }
      });
    });
  });
});
