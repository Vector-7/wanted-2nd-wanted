from django.urls import path

from company.views import CompanyCreateView, CompanyView, CompanySearchView

urlpatterns = [
    path('', CompanyCreateView.as_view()),
    path('/<str:company_name>', CompanyView.as_view()),
]
