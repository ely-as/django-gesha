import { PathInfo } from "./urls";

interface Context {
  _gesha?: {
    paths?: {
      [pathName: string]: PathInfo
    }
  };
  [key: string]: any;
}

export function getContext(id = "js_context_data"): Context {
  const el = document.querySelector(`#${id}`);
  if (el) {
    return JSON.parse(el.textContent);
  } else {
    console.warn(`Could not load context data from element with id '${id}'`);
    return {};
  }
}

export function loadContext() {
  this.context = getContext();
}

export interface ContextAPI {
  context?: Context;
  getContext: typeof getContext;
  loadContext?: typeof loadContext;
}
