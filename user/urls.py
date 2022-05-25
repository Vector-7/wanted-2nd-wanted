from django.urls import path

from user.views import UserCreateView, UserView

urlpatterns = [
    path('', UserCreateView.as_view()),
    path('/<str:name>', UserView.as_view()),
]
