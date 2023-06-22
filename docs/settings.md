## **django-gesha** Settings

---

### <pre>**GESHA_ALLOWED_URL_NAMES**</pre>

Default: `[]`

A list of allowed URL names for use in [reversing URLs](../user_guide/#reverse-urls).
Supports [Unix shell-style wildcards](https://docs.python.org/3/library/fnmatch.html)
<span style="white-space:nowrap;">(`*`, `?`, `[seq]` and `[!seq]`)</span>. Example to
match `login`, `logout` and all paths in the `myapp` namespace:

``` py
GESHA_ALLOWED_URL_NAMES = ["log*", "myapp:*"]
```

The default setting (an empty list) disables all patterns.

---
