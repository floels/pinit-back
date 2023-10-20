from django.urls import path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

from .views import authentication, signup, accounts, pins, search

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
    path("accounts/", accounts.get_accounts, name="get_accounts"),
    path(
        "pins/<int:unique_id>/",
        pins.GetPinDetailsView.as_view(),
        name="get_pin_details",
    ),
    path(
        "pins/suggestions/",
        pins.GetPinSuggestionsView.as_view(),
        name="get_pin_suggestions",
    ),
    path("search/", search.search_pins, name="search_pins"),
    path(
        "search/autocomplete/", search.autocomplete_search, name="search_autocomplete"
    ),
]
