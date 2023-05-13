from __future__ import annotations

from collections.abc import Iterable

from gesha import types
from gesha.conf import get_setting
from gesha.urls import get_paths_dict


class JSContextMixin:
    def get_js_context_data(self, **kwargs) -> dict:
        return {
            "_gesha": {
                "paths": get_paths_dict(
                    self.get_urlconf(), self.get_allowed_url_patterns()
                ),
            }
        }

    def get_allowed_url_patterns(self) -> Iterable[str]:
        return get_setting("GESHA_ALLOWED_URL_PATTERNS")

    def get_urlconf(self) -> types.URLConf | None:
        return None

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)  # type: ignore[misc]
        js_context_key = get_setting("GESHA_JSCONTEXT_KEY")
        context[js_context_key] = self.get_js_context_data(**kwargs)
        return context
