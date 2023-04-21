from django.conf import settings


def get_js_context_key() -> str:
    return getattr(settings, "GESHA_JSCONTEXT_KEY", "js_context_data")
