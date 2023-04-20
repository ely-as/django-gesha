// Single point of entry `django` for browser API
declare global {
    interface Window {
        django: object;
    }
}

export function setup(w: Window) {
    w.django = w.django || {};
}

if (typeof window !== "undefined") {
    setup(window);
}
