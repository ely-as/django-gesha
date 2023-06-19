export declare class Converter {
    readonly name: string;
    protected readonly reValidation: RegExp;
    constructor(name: string, reValidation: RegExp);
    check(value: number | string): boolean;
    convert(url: string, argName: string, value: number | string): string;
}
export declare class Converters {
    protected registered: {
        [name: string]: Converter;
    };
    static Converter: typeof Converter;
    constructor();
    get(name: string): Converter;
    register(converter: Converter): void;
}
