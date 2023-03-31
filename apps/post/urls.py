from django.urls import path

from .views import PostDetail, addpost

urlpatterns = [
    path('create/', addpost, name='post-create'),
    path('detail/<int:post_id>/', PostDetail, name='post-detail'), 
]
