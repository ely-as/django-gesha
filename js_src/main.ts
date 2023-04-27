import { getContext, loadContext, ContextAPI } from "./context";
import { URLs, UrlsAPI } from "./urls";

interface DjangoAPI extends ContextAPI, UrlsAPI {}

// Single point of entry `django` for browser API
declare global {
  interface Window {
    django: DjangoAPI;
  }
}

export function setup(w: Window) {
  w.django = w.django || {
    getContext: getContext,
    urls: new URLs()
  };

  // Shortcuts
  w.django.loadContext = loadContext.bind(w.django);
  w.django.reverse = URLs.prototype.reverse.bind(w.django.urls);

  // Load context when DOM is ready
  if (document.readyState === "complete") {
    w.django.loadContext();
  } else {
    w.document.addEventListener("DOMContentLoaded", () => {
      w.django.loadContext();
    });
  }
}

if (typeof window !== "undefined") {
  setup(window);
}
