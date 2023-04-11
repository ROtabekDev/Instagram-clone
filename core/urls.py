from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
                  path("admin/", admin.site.urls),
                  path("post/", include('apps.post.urls')),
                  path("", include('apps.main.urls')),
                  path("", include('apps.user.urls')),
                  path("", include('apps.story.urls')),

                  path('social-auth/', include('social_django.urls', namespace='social')),  # social auth
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
