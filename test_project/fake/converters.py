class FourDigitYearConverter:
    """Copied from
    https://docs.djangoproject.com/en/4.2/topics/http/urls/#registering-custom-path-converters
    """

    regex = "[0-9]{4}"

    def to_python(self, value):
        return int(value)

    def to_url(self, value):
        return "%04d" % value
