from django.urls import path
from .views import HomeView, ShowNotification

urlpatterns = [
    path("", HomeView.as_view(), name='home'),
    path("show-notification/", ShowNotification, name='show-notification'),
]
