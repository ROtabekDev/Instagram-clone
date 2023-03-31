from django.urls import path
from .views import HomeView, add_comment, ShowNotification

urlpatterns = [
    path("", HomeView.as_view(), name='home'),
    path("add-comment/", add_comment, name='add-comment'),
    path("show-notification/", ShowNotification, name='show-notification'),
]
