from __future__ import annotations

import typing

import django.urls

if typing.TYPE_CHECKING:
    ## for gesha.urls

    class PathInfo(typing.TypedDict):
        name: str
        route: str
        args: dict[str, str]

    Paths = dict[str, PathInfo]

    ## for django.urls.resolvers

    URLPattern = type[django.urls.URLPattern | django.urls.URLResolver]
    URLPatterns = list[URLPattern]

    class HasURLPatterns(typing.Protocol):
        urlpatterns: URLPatterns

    # urlconf can be either a module or dotted path to module
    # see comment: https://github.com/django/django/blob/3b4728310a7a64f8fcc548163b0aa5f98a5c78f5/django/urls/resolvers.py#L462
    # the above comment claims it can also be a list, but in practice this seems to
    # return an error (TypeError: unhashable type: 'list')
    URLConf = HasURLPatterns | str
