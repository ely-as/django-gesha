## Install to Python environment using pip

```sh
pip install django-gesha
```

## Install app in Django project

Add `gesha` to [`INSTALLED_APPS`](https://docs.djangoproject.com/en/4.2/ref/settings/#installed-apps) in your Django project's
[settings](https://docs.djangoproject.com/en/4.2/topics/settings/):
```py
INSTALLED_APPS = [
    ...
    "gesha",
]
```

## Collect JavaScript assets

Run the
[`collectstatic`](https://docs.djangoproject.com/en/4.2/ref/contrib/staticfiles/#collectstatic)
management command to collect django-gesha's JavaScript files. Django should locate
them automatically once the [app is installed](#install-app-in-django-project).
```sh
python manage.py collectstatic
```
