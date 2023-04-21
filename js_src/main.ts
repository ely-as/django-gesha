import { getContext } from "./context";

// Single point of entry `django` for browser API
declare global {
  interface Window {
    django: {
        context?: object
    };
  }
}

export function setup(w: Window) {
  w.django = w.django || {};
  w.document.addEventListener("DOMContentLoaded", () => {
    w.django.context = getContext();
  });
}

if (typeof window !== "undefined") {
  setup(window);
}
