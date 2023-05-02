export class Converter {
  public readonly name: string;
  protected readonly reValidation: RegExp;

  constructor(name: string, reValidation: RegExp) {
    this.name = name;
    this.reValidation = reValidation;
    if (reValidation.global) {
      // global regexes affect check()'s idempotence
      throw new TypeError("Validation RegExp for Converter cannot be global.");
    }
  }

  public check(value: number | string): boolean {
    return this.reValidation.test(String(value));
  }

  public convert(url: string, argName: string, value: number | string): string {
    // global ensures that multiple args of the same name are replaced
    const regExp = RegExp(`<${this.name}:${argName}>`, "g");
    return url.replace(regExp, String(value));
  }
}

const defaultConverters: Converter[] = [
  // copied from Python package Django (django.urls.converters)
  new Converter("int", /^[0-9]+$/),
  new Converter("path", /^.+$/),
  new Converter("slug", /^[-a-zA-Z0-9_]+$/),
  new Converter("str", /^[^/]+$/),
  new Converter("uuid", /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/)
];

export class Converters {
  protected registered: { [name: string]: Converter } = {};
  public static Converter = Converter;

  constructor() {
    for (const converter of defaultConverters) {
      this.register(converter);
    }
  }

  public get(name: string): Converter {
    return this.registered[name];
  }

  public register(converter: Converter) {
    this.registered[converter.name] = converter;
  }
}
