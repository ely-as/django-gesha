from __future__ import annotations

from collections.abc import Mapping

from gesha import mixins
from gesha.conf import get_setting


def create_js_context_data(extra_context: Mapping | None = None) -> dict:
    js_context = mixins.JSContextMixin().get_js_context_data()
    js_context.update(extra_context or {})
    js_context_key = get_setting("GESHA_JSCONTEXT_KEY")
    return {js_context_key: js_context}
