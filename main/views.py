from django.shortcuts import render

from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny

from main.serializers import CompanySerializer, RuleSerializer
from main.models.authenticate import Company, User
from main.models.rules import Rule
from main.models.calendars import Calendar

from main.filters import IsUserFilterBackend

from main.serializers import (
    CalendarSerializer
)


class UserMixin(object):
    permission_classes = (IsAuthenticated,)
    filter_backends = (IsUserFilterBackend, )

    def perform_create(self, serializer):
        serializer.save(user= self.request.user, company=self.request.user.company)

class CompanyListView(ListCreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = (AllowAny,)
    lookup_field = "uuid"

class RuleView(ListCreateAPIView):
    queryset = Rule.objects.all()
    serializer_class = RuleSerializer


class CalendarView(UserMixin, ListCreateAPIView):
    queryset = Calendar.objects.all()
    serializer_class = CalendarSerializer


