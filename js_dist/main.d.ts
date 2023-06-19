import { ContextAPI } from "./context";
import { UrlsAPI } from "./urls";
interface DjangoAPI extends ContextAPI, UrlsAPI {
}
declare global {
    interface Window {
        django: DjangoAPI;
    }
}
export declare function setup(w: Window): void;
export {};
