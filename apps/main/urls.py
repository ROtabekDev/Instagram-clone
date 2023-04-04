from django.urls import path

from apps.story.views import Stories_detail, create_story
from .views import HomeView, add_comment, ShowNotification 

urlpatterns = [
    path("", HomeView.as_view(), name='home'),

    path('stories-detail/<str:username>/', Stories_detail.as_view(), name='stories-detail'),
    path('create-story/', create_story, name='create-story'),

    path("add-comment/", add_comment, name='add-comment'),
    path("show-notification/", ShowNotification, name='show-notification'),
]
