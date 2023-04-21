export function getContext(id = "js_context_data") : any {
  const el = document.querySelector(`#${id}`);
  if (el) {
    return JSON.parse(el.textContent);
  } else {
    return {};
  }
}
