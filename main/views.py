from django.shortcuts import render

from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)
from rest_framework.permissions import IsAdminUser

from .serializers import CompanySerializer, RuleSerializer
from main.models.authenticate import Company
from main.models.rules import Rule

class CompanyListView(ListCreateAPIView):
    queryset = Company.objects.all()
    permission_classes = (IsAdminUser,)
    serializer_class = CompanySerializer
    lookup_field = "uuid"

class RuleView(ListCreateAPIView):
    queryset = Rule.objects.all()
    serializer_class = RuleSerializer


class CalendarView(ListCreateAPIView):
    pass


