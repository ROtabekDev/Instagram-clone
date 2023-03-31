from django.urls import path
from .views import sign_in, sign_up, sign_out, profile

urlpatterns = [
    path("sign-in/", sign_in, name='sign-in'),
    path("sign-up/", sign_up, name='sign-up'),
    path("sign-out/", sign_out, name='sign-out'),

    path("<str:username>/", profile, name='profile'),
]
