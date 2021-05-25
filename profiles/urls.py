from django.urls import path

from profiles.views import ProfileRetrieveAPIView

app_name = "profiles"

urlpatterns = [
    path('profiles/<username>', ProfileRetrieveAPIView.as_view(), name="profile")
]