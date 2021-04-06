from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register("event", views.EventViewSet)

urlpatterns = [
    path(
        route="company",
        view= views.CompanyListView.as_view(), 
        name= "company_list"
    ), 

    path(
        "calendar", 
        views.CalendarView.as_view(),
        name="calendar_list"
    ), 
    path(
        '', 
        include(router.urls)
    )
]