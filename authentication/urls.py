from django.urls import path
from rest_framework import routers

from authentication.views import RegistrationAPIView

app_name ="authentication"
urlpatterns = [
    path("users/", RegistrationAPIView.as_view(), name="register"),
]