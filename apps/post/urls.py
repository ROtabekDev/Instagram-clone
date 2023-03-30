from django.urls import path

from .views import addpost

urlpatterns = [
    path('create/', addpost, name='post-create'),
]
