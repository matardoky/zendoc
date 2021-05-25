from django.urls import path

from profiles.views import ProfileRetrieveAPIView, UserFollowAPIView, \
    FollowerRetrieve, FollowingRetrieve

app_name = "profiles"

urlpatterns = [
    path('profiles/<username>', ProfileRetrieveAPIView.as_view(), name="profile"),
    path('profiles/<username>/follow/', UserFollowAPIView.as_view()),
    path('followers/', FollowerRetrieve.as_view()),
    path('following/', FollowingRetrieve.as_view())
]