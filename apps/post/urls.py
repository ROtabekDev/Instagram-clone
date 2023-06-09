from django.urls import path

from .views import PostDetail, addpost, create_savedpost, delete_savedpost, deletepost

urlpatterns = [
    path('create/', addpost, name='post-create'),
    path('detail/<int:post_id>/', PostDetail, name='post-detail'),
    path('delete/<int:post_id>/', deletepost, name='post-delete'),

    path('create-savedpost/<int:post_id>/', create_savedpost, name='create-savedpost'), 
    path('delete-savedpost/<int:post_id>/', delete_savedpost, name='delete-savedpost'), 
]
