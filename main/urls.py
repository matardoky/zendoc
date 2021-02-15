from django.urls import path

from . import views

urlpatterns = [
    path(
        route="",
        view= views.CompanyListView.as_view(), 
        name= "company_list"
    ), 
    path(
        "test",
        views.RuleView.as_view(),
        name="rule_params"
    )
]