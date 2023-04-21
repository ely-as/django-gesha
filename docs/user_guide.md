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
