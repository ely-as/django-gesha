from __future__ import annotations

from django.views.generic import TemplateView

from gesha.mixins import JSContextMixin


class FakeView(JSContextMixin, TemplateView):
    template_name = "test.html"

    def get_js_context_data(self, **kwargs) -> dict:
        context = super().get_js_context_data(**kwargs)
        context.update(
            {
                "myNumber": 5,
                "myString": "this is a string",
            }
        )
        return context
