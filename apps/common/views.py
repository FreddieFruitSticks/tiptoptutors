from django.views.generic import TemplateView

class HomeView(TemplateView):
    template_name = "common/index.html"

class AboutView(TemplateView):
    template_name = "common/about.html"