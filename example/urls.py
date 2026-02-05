from django.urls import include, path
from django.views.generic import TemplateView

urlpatterns = [
    path("", TemplateView.as_view(template_name="example/home.html"), name="home"),
    path("__reload__/", include("django_browser_reload.urls")),
]
