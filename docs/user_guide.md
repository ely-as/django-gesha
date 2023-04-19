## Load django-gesha JavaScript assets in template

To use django-gesha's JavaScript API, load the script in your template:
```
{% load static %}

<script src="{% static 'gesha/dist/js/django-gesha.bundle.min.js' %}">
</script>
```
