from __future__ import annotations

import posixpath
import re
from collections.abc import Iterator
from urllib.parse import urljoin

from django.urls import URLPattern, URLResolver, get_resolver, get_urlconf

from gesha import types

RE_CONVERTER: re.Pattern = re.compile(r"<(\w+):(\w+)>")


def get_args(route: str) -> dict[str, str]:
    """Get a map of URL arg names to their converter names."""
    return {name: type for type, name in re.findall(RE_CONVERTER, route)}


def namejoin(*names: str) -> str:
    """Create a namespaced URL from its parts e.g. `polls:index`."""
    return ":".join([n for n in names if n])


def pathjoin(*paths: str) -> str:
    """Create the path component of a URL from its segments."""
    return urljoin("/", posixpath.join("", *paths))


def iter_patterns(  # noqa: C901 (complexity: 6 > 5)
    resolver_or_pattern: types.URLPattern,
    name: list[str] | None = None,
    route: list[str] | None = None,
) -> Iterator[types.PathInfo]:
    # Initialize defaults
    name = name or []
    route = route or []
    # Find current route
    this_route_segment = getattr(resolver_or_pattern.pattern, "_route", "")
    current_route = route[:] + [this_route_segment]
    # Yield if this is a URL pattern and it has a name (can't reverse unnamed paths)
    if isinstance(resolver_or_pattern, URLPattern):
        if this_name := resolver_or_pattern.name:
            name_str = namejoin(*name, this_name)
            route_str = pathjoin(*current_route)
            yield {
                "name": name_str,
                "route": route_str,
                "args": get_args(route_str),
            }
    # Recurse if this is a URL resolver
    elif isinstance(resolver_or_pattern, URLResolver):
        current_name = name[:]
        if this_namespace := resolver_or_pattern.namespace:
            current_name.append(this_namespace)
        for url_pattern in resolver_or_pattern.url_patterns:
            yield from iter_patterns(url_pattern, current_name, current_route)


def get_paths_dict(urlconf: types.URLConf | None = None) -> types.Paths:
    if urlconf is None:
        urlconf = get_urlconf()
    resolver = get_resolver(urlconf)
    return {p["name"]: p for p in iter_patterns(resolver)}
