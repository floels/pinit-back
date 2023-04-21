from django.urls import path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .views import authentication, signup

schema_view = get_schema_view(
    openapi.Info(
        title="PinIt API",
        default_version="v1",
        license=openapi.License(name="Apache 2.0"),
    ),
    public=True,
)

urlpatterns = [
    path(
        "redoc/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
    path("signup/", signup.SignupView.as_view(), name="signup"),
    path("token/", authentication.TokenObtainPairView.as_view(), name="token_obtain"),
    path(
        "token/refresh/",
        authentication.TokenRefreshView.as_view(),
        name=("token_refresh"),
    ),
]
