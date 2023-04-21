import logging
import typing

from django import template
from django.utils.html import json_script

from gesha.settings import get_js_context_key

logger = logging.getLogger(__name__)
register = template.Library()


@register.simple_tag(takes_context=True)
def jscontext(context: typing.Mapping) -> str:
    js_context_key = get_js_context_key()
    try:
        js_context = context[js_context_key]
    except KeyError:
        logger.warning(
            "Template tag 'gesha' used, but context dict did not contain key "
            f"'{js_context_key}'."
        )
        js_context = {}
    return json_script(js_context, js_context_key)
