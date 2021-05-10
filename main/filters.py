# from rest_framework import filters

# class IsUserFilterBackend(filters.BaseFilterBackend): 
#     def filter_queryset(self, request, queryset, view):
#         return queryset.filter(user= request.user)

# class CompanyFilterBackend(filters.BaseFilterBackend):
#     def filter_queryset(self, request, queryset, view):
#         return queryset.filter(company= request.user.company)