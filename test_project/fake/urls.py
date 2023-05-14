from __future__ import annotations

from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path, register_converter

from . import converters, views

register_converter(converters.FourDigitYearConverter, "yyyy")

view = views.FakeView.as_view()  # shortcut

fake_urlpatterns: list = [
    path("", view, name="test"),
    path("func-based/", views.function_based_view, name="test_func_based"),
    path("async/", views.async_view, name="test_async"),
    # mainly for JS tests
    path("page/<int:num>", view, name="page"),
    path("<slug:slug>/<int:num>", view, name="named_page"),
    path("articles/<yyyy:year>", view, name="custom_converter"),
]

if settings.DEBUG:
    fake_urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns: list = [
    # ensure that URLs are namespaced
    path("", include((fake_urlpatterns, "fake"))),
]
