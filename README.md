# django-gesha ☕

[![Test](https://github.com/ely-as/django-gesha/actions/workflows/test.yml/badge.svg?branch=main)](https://github.com/ely-as/django-gesha/actions/workflows/test.yml)

JavaScript utilities for [Django](https://www.djangoproject.com/) projects.

## Installation

### Install to Python environment using pip

```sh
pip install git+https://github.com/ely-as/django-gesha
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

## Contributing

See [Contributing](docs/contributing.md).

## License

[MIT](https://github.com/ely-as/django-gesha/blob/main/LICENSE).
