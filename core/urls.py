from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("", include('apps.main.urls')),
    path("user/", include('apps.user.urls')),
    path("post/", include('apps.post.urls')),
    path("story/", include('apps.story.urls')),
    path("admin/", admin.site.urls),
]
