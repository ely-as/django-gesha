## Basic setup

Once **django-gesha** [has been installed](../installation/) it can be enabled by
configuring the [views](#configure-views) and [templates](#configure-templates) you
would like to use it with.

### Configure views

Add `#!py gesha.mixins.JSContextMixin` to your class-based view, and add JavaScript
context data by extending its `#!py get_js_context_data()` method:

!!! example "Example inclusion of `#!py JSContextMixin`"

    === "myapp/views.py"

        ``` py hl_lines="2 5 8" linenums="1"
        from django.views.generic import TemplateView
        from gesha.mixins import JSContextMixin


        class HomeView(JSContextMixin, TemplateView):
            template_name = "myapp/home.html"

            def get_js_context_data(self, **kwargs) -> dict:
                context = super().get_js_context_data(**kwargs)
                context.update({"myNumber": 5, "myString": "this is my string"})
                return context
        ```

    === "myapp/urls.py"

        ``` py linenums="1"
        from django.urls import path
        from myapp import views

        urlpatterns = [
            path("", views.HomeView.as_view(), name="home"),
        ]
        ```

### Configure templates

To use **django-gesha**'s JavaScript API, load the script in your template, and load the
context using the `#!django {% jscontext %}` template tag:

``` django
{% load gesha static %}

{% jscontext %}

<script src="{% static 'gesha/dist/js/django-gesha.bundle.min.js' %}"></script>
```

??? example "Example of a whole template"

    ``` django title="myapp/templates/myapp/home.html"
    <!doctype html>
    <html lang="en">
      <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <title>Home</title>
      </head>
      <body>
        {% load gesha static %}

        {% jscontext %}

        <script src="{% static 'gesha/dist/js/django-gesha.bundle.min.js' %}">
        </script>
      </body>
    </html>
    ```

### Test JavaScript API

You can test that the JavaScript API is available by opening the console on your
browser:

``` js
>> console.log(django.context.myNumber)
   5

>> console.log(django.context.myString)
   "this is my string"
```

## Using the JavaScript API

### Add context

Override `#!py get_js_context_data()` to add context data. Data added here must be JSON
serializable.

!!! example

    ``` py title="view"
    class HomeView(JSContextMixin, TemplateView):
        template_name = "myapp/home.html"

        def get_js_context_data(self, **kwargs) -> dict:
            context = super().get_js_context_data(**kwargs)
            context.update({"myNumber": 5, "myString": "this is my string"})
            return context
    ```

### Reverse URLs

Reverse URLs in JavaScript using the following function:

`#!ts django.urls.reverse(name: string, kwargs?: ReverseKwargs): string`

  - `#!ts name: string` – The namespaced URL name.
  - `#!ts kwargs?: { [argName: string]: number | string }` – URL arguments.

!!! example "Examples of URL reversing"

    ``` js
    >> django.urls.reverse("myapp:home")
    "/"

    >> django.reverse("myapp:page", { page: 5 })
    "/page/5/"
    ```

    ??? info "Equivalent code in Django"

        ``` py title="In Python"
        from django.urls import reverse

        reverse("myapp:page", kwargs={"page": 5})
        ```

        ``` django title="In templates"
        {% url 'myapp:page' page=5 %}
        ```

!!! tip

    `#!js django.urls.reverse()` is aliased to `#!js django.reverse()`
