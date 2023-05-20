from __future__ import annotations

from collections.abc import Iterable

from django.conf import settings


class SettingDefaults:
    GESHA_JSCONTEXT_KEY: str = "js_context_data"
    GESHA_ALLOWED_URL_PATTERNS: Iterable[str] = []


def get_setting(name: str) -> str | Iterable[str]:
    try:
        default = getattr(SettingDefaults, name)
        return getattr(settings, name, default)
    except AttributeError:
        raise ValueError(f"'{name}' is not a valid gesha setting") from None
