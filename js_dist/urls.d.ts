import { Converter, Converters } from "./converters";
export interface PathInfo {
    args: {
        [argName: string]: string;
    };
    name?: string;
    route: string;
}
interface ReverseKwargs {
    [argName: string]: number | string;
}
declare class NoReverseMatch extends Error {
    constructor(message: string, urlName?: string);
}
export declare class URLs {
    protected paths: {
        [pathName: string]: PathInfo;
    };
    Converter: typeof Converter;
    NoReverseMatch: typeof NoReverseMatch;
    readonly converters: Converters;
    constructor();
    protected getPathInfo(name: string): PathInfo;
    reverse(name: string, kwargs?: ReverseKwargs): string;
}
export interface UrlsAPI {
    reverse?: typeof URLs.prototype.reverse;
    urls?: URLs;
}
export {};
