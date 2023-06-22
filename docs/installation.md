!!! tip "Starting a new project?"

    Consider using
    [**django-gesha-template**](https://github.com/ely-as/django-gesha-template), which
    is pre-configured with **django-gesha** and a pipeline for TypeScript integration.

## Install to Python environment using pip

``` console
$ pip install django-gesha
```

## Install app in Django project

Add `gesha` to
[`INSTALLED_APPS`](https://docs.djangoproject.com/en/stable/ref/settings/#installed-apps)
in your Django project's
[settings](https://docs.djangoproject.com/en/stable/topics/settings/):

``` py title="settings.py" hl_lines="3"
INSTALLED_APPS = [
    ...
    "gesha",
]
```

## Collect JavaScript assets

Run [`collectstatic`](https://docs.djangoproject.com/en/stable/ref/contrib/staticfiles/#collectstatic)
to collect **django-gesha**'s JavaScript files.

``` console
$ python manage.py collectstatic
```

??? tip "Static file discovery"

    Django should locate **django-gesha**'s JavaScript files automatically once the
    [app is installed](#install-app-in-django-project).

    To check that the JavaScript bundle has been collected:

    === "POSIX"

        ``` console
        $ python manage.py findstatic gesha/dist/js/django-gesha.bundle.min.js
        ```

    === "Windows"

        ``` doscon
        C:\> python manage.py findstatic gesha\dist\js\django-gesha.bundle.min.js
        ```

## Advanced

### Install to Node.js environment

``` console
$ npm install https://github.com/ely-as/django-gesha
```

### Import in TypeScript

For example, in your main entry-point:

``` ts title="main.ts"
import "django-gesha";

...
```

This would eliminate the need to [collect JavaScript assets](#collect-javascript-assets)
and load them in your HTML template.
