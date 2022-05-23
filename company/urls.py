from django.urls import path

from company.views import CompanyCreateView

urlpatterns = [
    path('', CompanyCreateView.as_view())
]
