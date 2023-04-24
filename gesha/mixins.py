from __future__ import annotations

from gesha.conf import get_setting


class JSContextMixin:
    def get_js_context_data(self, **kwargs) -> dict:
        return {}

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)  # type: ignore[misc]
        js_context_key = get_setting("GESHA_JSCONTEXT_KEY")
        context[js_context_key] = self.get_js_context_data(**kwargs)
        return context
