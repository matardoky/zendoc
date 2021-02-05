from django.shortcuts import render

from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)
from rest_framework.permissions import IsAuthenticated

from .serializers import CompanySerializer
from main.models.users import Company

class CompanyListView(ListCreateAPIView):
    queryset = Company.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = CompanySerializer
    lookup_field = "uuid"


