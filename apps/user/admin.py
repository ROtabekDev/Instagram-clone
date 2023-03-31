from django.contrib import admin
from apps.user.models import *

admin.site.register(CustomUser)
admin.site.register(UserFollower)
admin.site.register(HashTag)
admin.site.register(HashTagFollower)