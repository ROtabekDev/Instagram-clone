from django.contrib import admin

from .models import Story, StoryContent, StoryViewed

admin.site.register(Story)
admin.site.register(StoryContent)
admin.site.register(StoryViewed)
