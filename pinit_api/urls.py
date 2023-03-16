from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .views import TokenObtainView

schema_view = get_schema_view(
    openapi.Info(
        title="PinIt API",
        default_version="v1",
        license=openapi.License(name="Apache 2.0"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path(
        "redoc/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
    path("token/", TokenObtainView.as_view(), name="token_obtain"),
    path("token/refresh/", TokenRefreshView.as_view(), name=("token_refresh")),
]
