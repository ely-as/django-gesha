import { readFileSync } from "fs";
import { resolve } from "path";

export function loadText(fp: string) : string {
  return readFileSync(resolve(__dirname, fp), "utf-8");
}
