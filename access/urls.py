from django.urls import path

from access.views import LoginView, CertificateView

urlpatterns = [
    path('login', LoginView.as_view()),
    path('certificate', CertificateView.as_view()),
]