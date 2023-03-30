from django.contrib import admin

from .models import *

admin.site.register(Post)
admin.site.register(PostFileContent)
admin.site.register(Location)
admin.site.register(Hashtag)
admin.site.register(PostHastag)
admin.site.register(SpecifiedUser)
