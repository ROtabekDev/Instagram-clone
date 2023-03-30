from django.contrib import admin
from apps.user.models import CustomUser, UserFollower

admin.site.register(CustomUser)
admin.site.register(UserFollower)