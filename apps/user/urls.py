from django.urls import path
from .views import (
    sign_in, sign_up, sign_out, profile, follow, unfollow, 
    remove_follower, remove_following, MessageView, sms_code,
    create_like, remove_like, edit_profile, create_chat
    )

urlpatterns = [
    path("message/", MessageView.as_view(), name='message'),
    path("message/<str:name>/", MessageView.as_view(), name='message'),
    path("create_chat/<str:user_id>/", create_chat, name='create-chat'),
    path("sign-in/", sign_in, name='sign-in'),
    path("sign-up/", sign_up, name='sign-up'),
    path("sign-out/", sign_out, name='sign-out'),
    path("sms-code/", sms_code, name='sms-code'),

    path("<str:username>/", profile, name='profile'),
    path('<str:username>/saved/', profile, name='profile-favourite'),
    
    path("follow/<str:username>/", follow, name='follow_user'),
    path("unfollow/<str:username>/", unfollow, name='unfollow_user'),

    path("remove-follower/<str:username>/", remove_follower, name='remove_follower'), 
    path("remove-following/<str:username>/", remove_following, name='remove_following'),

    path("create-like/<int:post_id>/", create_like, name='create_like'), 
    path("remove-like/<int:post_id>/", remove_like, name='remove_like'), 

    path('profile/edit/', edit_profile, name="edit-profile"),
    # path("message/", MessageView.as_view(), name='message'),
]