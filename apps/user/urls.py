from django.urls import path
from .views import sign_in, sign_up, sign_out, profile, follow, unfollow, MessageView, sms_code

urlpatterns = [
    path("sign-in/", sign_in, name='sign-in'),
    path("sign-up/", sign_up, name='sign-up'),
    path("sign-out/", sign_out, name='sign-out'),
    path("sms-code/", sms_code, name='sms-code'),

    path("<str:username>/", profile, name='profile'),
    path("follow/<str:username>/", follow, name='follow_user'),
    path("unfollow/<str:username>/", unfollow, name='unfollow_user'),

    # path("message/", MessageView.as_view(), name='message'),
]
