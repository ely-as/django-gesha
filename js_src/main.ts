// Single point of entry `django` for browser API
declare global {
    interface Window {
        django: any;
    }
}

window.django = window.django || {};

// Declare that this is a module - can be removed when we add imports
export {};
