from django.urls import path, include
from drf_spectacular.views import SpectacularSwaggerView, SpectacularAPIView

urlpatterns = [
    # API documentation
    path("", SpectacularSwaggerView.as_view(url_name="schema")),
    path("schema", SpectacularAPIView.as_view(), name="schema"),

    # Application urls
    path("", include("app.urls")),
]
