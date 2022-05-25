from django.urls import path

from company.views import CompanySearchView

urlpatterns = [
    path(f'/companies', CompanySearchView.as_view()),
]