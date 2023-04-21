import typing

from gesha.settings import get_js_context_key


class JSContextMixin:
    def get_js_context_data(self, **kwargs) -> typing.Dict:
        return {}

    def get_context_data(self, **kwargs) -> typing.Dict:
        context = super().get_context_data(**kwargs)  # type: ignore[misc]
        js_context_key = get_js_context_key()
        context[js_context_key] = self.get_js_context_data(**kwargs)
        return context
