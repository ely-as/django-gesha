from __future__ import annotations

from django.conf import settings

DEFAULTS: dict[str, str] = {
    "GESHA_JSCONTEXT_KEY": "js_context_data",
}


def get_setting(name: str) -> str:
    if name not in DEFAULTS:
        raise ValueError(f"'{name}' is not a valid gesha setting")
    return getattr(settings, name, DEFAULTS[name])
