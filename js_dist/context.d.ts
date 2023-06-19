import { PathInfo } from "./urls";
interface Context {
    _gesha?: {
        paths?: {
            [pathName: string]: PathInfo;
        };
    };
    [key: string]: any;
}
export declare function getContext(id?: string): Context;
export declare function loadContext(): void;
export interface ContextAPI {
    context?: Context;
    getContext: typeof getContext;
    loadContext?: typeof loadContext;
}
export {};
