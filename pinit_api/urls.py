from django.urls import path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

from .views import (
    accounts,
    authentication,
    create_pin,
    pin_suggestions,
    pins,
    search_suggestions,
    search,
    signup,
)

urlpatterns = [
    # API documentation
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "schema/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"
    ),
    path("signup/", signup.sign_up, name="sign_up"),
    path(
        "token/obtain/",
        authentication.TokenObtainPairView.as_view(),
        name="obtain_token",
    ),
    path(
        "token/refresh/",
        authentication.TokenRefreshView.as_view(),
        name=("refresh_token"),
    ),
    path(
        "accounts/me/",
        accounts.GetMyAccountDetailsView.as_view(),
        name="get_my_account_details",
    ),
    path(
        "accounts/<str:username>/",
        accounts.GetAccountDetailsView.as_view(),
        name="get_account_details",
    ),
    path(
        "pins/<str:unique_id>/",
        pins.GetPinDetailsView.as_view(),
        name="get_pin_details",
    ),
    path(
        "pin-suggestions/",
        pin_suggestions.GetPinSuggestionsView.as_view(),
        name="get_pin_suggestions",
    ),
    path("search/", search.search_pins, name="search_pins"),
    path(
        "search-suggestions/",
        search_suggestions.get_search_suggestions,
        name="get_search_suggestions",
    ),
    path("create-pin/", create_pin.CreatePinView.as_view(), name="create_pin"),
]
