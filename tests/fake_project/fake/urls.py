from __future__ import annotations

from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

from . import views

fake_urlpatterns: list = [path("", views.FakeView.as_view(), name="test")]

if settings.DEBUG:
    fake_urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns: list = [
    # ensure that URLs are namespaced
    path("", include((fake_urlpatterns, "fake"))),
]
