from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register("event", views.EventViewSet)
router.register("calendar", views.CalendarViewSet)

urlpatterns = [
    path(
        route="company",
        view= views.CompanyListView.as_view(), 
        name= "company_list"
    ), 
    path(
        "event_list", 
        views.EventAPIView.as_view()
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