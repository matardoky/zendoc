from django.urls import path
from rest_framework import routers

from authentication.views import (
    RegistrationAPIView, Activate
)

app_name ="authentication"
urlpatterns = [
    path("users/", RegistrationAPIView.as_view(), name="register"),
    path('activate/<uidb64>/<token>/', Activate.as_view(), name="activate"),
    
]