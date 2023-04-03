from django.urls import path

from .views import sign_in, sign_up, sign_out, profile, sms_code, MessageView, create_chat

urlpatterns = [
    path("message/", MessageView.as_view(), name='message'),
    path("message/<str:name>/", MessageView.as_view(), name='message'),
    path("create_chat/<str:user_id>/", create_chat, name='create-chat'),
    path("sign-in/", sign_in, name='sign-in'),
    path("sign-up/", sign_up, name='sign-up'),
    path("sign-out/", sign_out, name='sign-out'),
    path("sms-code/", sms_code, name='sms-code'),

    path("<str:username>/", profile, name='profile'),

]
