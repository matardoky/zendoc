from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register("event", views.EventViewSet)
router.register("calendar", views.CalendarViewSet)
router.register("motifs", views.MotifViewSet)

urlpatterns = [
    path(
        route="company",
        view= views.CompanyListView.as_view(), 
        name= "company"
    ), 
    path(
        route="events", 
        view = views.EventAPIView.as_view(),
        name="events_list"
    ),

    re_path(
        '', 
        include(router.urls)
    ), 
    path(
        "occurrences",
        views.api_occurrences,
        name="occurrence"
    )
]