from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("user/", include('apps.user.urls')),
    path("story/", include('apps.story.urls')),
    path("admin/", admin.site.urls),
]
