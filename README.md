# django-gesha ☕

[![Test](https://github.com/ely-as/django-gesha/actions/workflows/test.yml/badge.svg?branch=main)](https://github.com/ely-as/django-gesha/actions/workflows/test.yml)
![Version](https://img.shields.io/pypi/v/django-gesha)
![Python](https://img.shields.io/pypi/pyversions/django-gesha)
![Django](https://img.shields.io/pypi/djversions/django-gesha)

JavaScript utilities for [Django](https://www.djangoproject.com/) projects.

**Current features:**

  - Easily add JavaScript context in class-based views and access it via a JavaScript API.
  - Reverse URLs in JavaScript (instead of using `reverse` in Python, or `url` in templates).

Many more [features are planned](https://github.com/ely-as/django-gesha/labels/feature) ✍️.

## Installation

### Install to Python environment using pip

```sh
pip install django-gesha
```

### Install app in Django project

Add `gesha` to [`INSTALLED_APPS`](https://docs.djangoproject.com/en/4.2/ref/settings/#installed-apps) in your Django project's
[settings](https://docs.djangoproject.com/en/4.2/topics/settings/):
```py
INSTALLED_APPS = [
    ...
    "gesha",
]
```

### Collect JavaScript assets

Run the
[`collectstatic`](https://docs.djangoproject.com/en/4.2/ref/contrib/staticfiles/#collectstatic)
management command to collect django-gesha's JavaScript files. Django should locate
them automatically once the [app is installed](#install-app-in-django-project).
```sh
python manage.py collectstatic
```

## Basic usage

### Add mixin to class-based view

For example:
```py
from django.views.generic import TemplateView
from gesha.mixins import JSContextMixin


class MyPage(JSContextMixin, TemplateView):
    template_name = "myapp/mypage.html"

    def get_js_context_data(self, **kwargs) -> typing.Dict:
        context = super().get_js_context_data(**kwargs)
        context.update({
            "myNumber": 5,
            "myString": "this is my string",
        })
        return context
```

### Load django-gesha JavaScript assets in template

To use django-gesha's JavaScript API, load the script in your template, and load the
context using the `jscontext` template tag:
```
{% load gesha static %}

{% jscontext %}

<script src="{% static 'gesha/dist/js/django-gesha.bundle.min.js' %}">
</script>
```

### Test in JavaScript

Access the context data using the `django` JavaScript API:
```js
>> console.log(django.context.myNumber)
   5

>> console.log(django.context.myString)
   "this is my string"
```

## Contributing

See [Contributing](https://django-gesha.readthedocs.io/en/latest/contributing/).

## License

[MIT](https://github.com/ely-as/django-gesha/blob/main/LICENSE).
