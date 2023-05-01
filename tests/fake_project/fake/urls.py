from __future__ import annotations

from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

from . import views

view = views.FakeView.as_view()  # shortcut

fake_urlpatterns: list = [
    path("", view, name="test"),
    path("page/<int:num>", view, name="page"),
]

if settings.DEBUG:
    fake_urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns: list = [
    # ensure that URLs are namespaced
    path("", include((fake_urlpatterns, "fake"))),
]
