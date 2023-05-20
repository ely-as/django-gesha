from __future__ import annotations

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView

import gesha

TEMPLATE_NAME = "test.html"
CONTEXT = {
    "myNumber": 5,
    "myString": "this is a string",
}


class FakeView(gesha.JSContextMixin, TemplateView):
    template_name = TEMPLATE_NAME

    def get_js_context_data(self, **kwargs) -> dict:
        context = super().get_js_context_data(**kwargs)
        context.update(CONTEXT)
        return context


def function_based_view(request: HttpRequest) -> HttpResponse:
    context = gesha.create_js_context_data(CONTEXT)
    return render(request, TEMPLATE_NAME, context=context)


# Async views


async def async_view(request: HttpRequest) -> HttpResponse:
    context = {}
    js_context = gesha.create_js_context_data(CONTEXT)
    context.update(js_context)
    return render(request, TEMPLATE_NAME, context=context)
