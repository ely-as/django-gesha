from django.views.generic import TemplateView


class FakeView(TemplateView):
    template_name = "test.html"
