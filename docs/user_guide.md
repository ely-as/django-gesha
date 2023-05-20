## Basic setup

Once **django-gesha** [has been installed](../installation/) it can be enabled by
configuring the [views](#configure-views) and [templates](#configure-templates) you
would like to use it with.

### Configure views

**django-gesha** requires you to add some context data to your views to work. See the
following examples for class-based views and function-based views.

!!! example "Example class-based view"

    Add `#!py gesha.JSContextMixin` to your class-based view, and add JavaScript context
    data by extending its `#!py get_js_context_data()` method:

    === "myapp/views.py"

        ``` py hl_lines="2 5 8 9 10 11" linenums="1"
        import gesha
        from django.views.generic import TemplateView


        class HomeView(gesha.JSContextMixin, TemplateView):
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

!!! example "Example function-based view"

    === "myapp.views.py"

        ``` py hl_lines="3 9 10 11" linenums="1"
        import gesha
        from django.http import HttpRequest, HttpResponse
        from django.shortcuts import render


        def home(request: HttpRequest) -> HttpResponse:
            context = {}
            context.update(
                gesha.create_js_context_data(
                    {"myNumber": 5, "myString": "this is my string"}
                )
            )
            return render(request, "myapp/home.html", context=context)
        ```

    === "myapp/urls.py"

        ``` py linenums="1"
        from django.urls import path
        from myapp import views

        urlpatterns = [
            path("", views.home, name="home"),
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

Any context data added using the methods below must be JSON serializable.

!!! example "Adding context in class-based views"

    For class-based views override `#!py get_js_context_data()` to add context data:

    ``` py
    class HomeView(gesha.JSContextMixin, TemplateView):
        template_name = "myapp/home.html"

        def get_js_context_data(self, **kwargs) -> dict:
            context = super().get_js_context_data(**kwargs)
            context.update({"myNumber": 5, "myString": "this is my string"})
            return context
    ```

!!! example "Adding context in class-based views"

    For function-based views pass a dict to `#!py create_js_context_data()` to add
    context data:

    ``` py
    def home(request):
        context = {}
        context.update(
            gesha.create_js_context_data(
                {"myNumber": 5, "myString": "this is my string"}
            )
        )
        return render(request, "myapp/home.html", context=context)
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

    To set the URLs available for reversing configure the
    [`GESHA_ALLOWED_URL_PATTERNS`](../settings/#gesha_allowed_url_patterns) setting.

    These patterns can also be set in class-based views by overriding the
    `#!py get_allowed_url_patterns()` method, for example:

    ``` py
    class HomeView(gesha.JSContextMixin, TemplateView):
        ...

        def get_allowed_url_patterns(self):
            return ["myapp:home", "otherapp:*"]
    ```

!!! tip

    `#!js django.urls.reverse()` is aliased to `#!js django.reverse()`

#### Custom converters

If you have
[registered custom path converters](https://docs.djangoproject.com/en/stable/topics/http/urls/#registering-custom-path-converters)
in your Django project, you can also register them using the JavaScript API, for
example:

!!! example "Example path converter registration"

    === "JavaScript"

        ``` js linenums="1"
        const fourDigitYearConverter = new django.urls.Converter("yyyy", /[0-9]{4}/);

        django.urls.converters.register(fourDigitYearConverter);
        ```

    === "Python"

        ``` py linenums="1"
        class FourDigitYearConverter:
            regex = "[0-9]{4}"

            def to_python(self, value):
                return int(value)

            def to_url(self, value):
                return "%04d" % value
        ```

#### Handling errors

`#!js django.reverse()` will throw a `#!js django.urls.NoReverseMatch` error if:

  - The name provided does not match any known URLs.
  - The URL requires args, but none were provided.
  - The URL received args, but their values failed validation.

??? example "Example JavaScript code which handles `#!js NoReverseMatch`"

    ``` js hl_lines="5" linenums="1"
    try {
      django.urls.reverse("missing:path")
    }
    catch(err) {
      if (err.name === "NoReverseMatch") {
        console.log("handle NoReverseMatch");
      } else {
        console.log("handle different error")
      }
    }
    ```
