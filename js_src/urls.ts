import { Converter, Converters } from "./converters";

export interface PathInfo {
  args: { [argName: string]: string };
  name?: string;
  route: string;
}

interface ReverseKwargs {
  [argName: string]: number | string;
}

class NoReverseMatch extends Error {
  constructor(message: string, urlName?: string) {
    if (urlName !== undefined) {
      message = `Reverse for '${urlName}' failed: ${message}`;
    }
    super(message);
    this.name = "NoReverseMatch";
  }
}

export class URLs {
  protected paths: { [pathName: string]: PathInfo } = {};
  public Converter = Converter;
  public NoReverseMatch = NoReverseMatch;
  public readonly converters: Converters;

  constructor() {
    this.converters = new Converters();
  }

  protected getPathInfo(name: string): PathInfo {
    if (name in this.paths) {
      return this.paths[name];
    } else {
      return window.django.context._gesha.paths[name];
    }
  }

  public reverse(name: string, kwargs?: ReverseKwargs): string {
    // Find path
    const path = this.getPathInfo(name);
    if (path === undefined) {
      throw new NoReverseMatch("not found", name);
    }
    // Insert kwargs into unformatted URL
    let url = path.route;
    // For all required args
    for (const [argName, converterName] of Object.entries(path.args)) {
      // Check that user passed this arg
      if ((kwargs === undefined) || !(argName in kwargs)) {
        const argNames = Object.keys(path.args).join(", ");
        throw new NoReverseMatch(`missing keyword arguments (${argNames})`, name);
      }
      // Get the converter
      const converter = this.converters.get(converterName);
      const value = kwargs[argName];
      // Validate arg with converter
      if (!(converter.check(value))) {
        throw new NoReverseMatch(`'${value}' is not a '${converterName}'`, name);
      }
      // Insert arg into URL
      url = converter.convert(url, argName, value);
    }
    return url;
  }
}

export interface UrlsAPI {
  reverse?: typeof URLs.prototype.reverse;
  urls?: URLs;
}
