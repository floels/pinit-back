from django.urls import path
from .views import obtain_token_pair
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("token/", obtain_token_pair, name="token_obtain"),
    path("token/refresh/", TokenRefreshView.as_view(), name=("token_refresh")),
]
