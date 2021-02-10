from django.shortcuts import render

from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)
from rest_framework.permissions import IsAdminUser

from .serializers import CompanySerializer
from main.models.authenticate import Company

class CompanyListView(ListCreateAPIView):
    queryset = Company.objects.all()
    permission_classes = (IsAdminUser,)
    serializer_class = CompanySerializer
    lookup_field = "uuid"


