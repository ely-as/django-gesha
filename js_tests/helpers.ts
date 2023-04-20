import { readFileSync } from "fs";
import { JSDOM } from "jsdom"
import { resolve } from "path";

function loadText(fp: string): string {
  return readFileSync(resolve(__dirname, fp), "utf-8");
}

export function loadDOMFromFile(fp: string) {
  return new Promise(resolve => {
    const { window } = new JSDOM(loadText(fp)) as unknown as Window;
    global.window = window;
    global.document = window.document;
    window.addEventListener("load", resolve);
  });
}

export function cleanDOM() {
  delete global.window;
  delete global.document;
}
