from django.contrib import admin
from apps.user.models import *


class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "chat", "sender", "msg", "is_read")
    list_display_links = ("id", "chat")
    search_fields = ("chat", "sender", "msg")
    date_hierarchy = "created_at"


admin.site.register(CustomUser)
admin.site.register(UserFollower)
admin.site.register(HashTag)
admin.site.register(HashTagFollower)

admin.site.register(Chat)
admin.site.register(Participant)
admin.site.register(Message, MessageAdmin)
