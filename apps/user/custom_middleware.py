from datetime import datetime, timedelta
from django.conf import settings
from django.utils import timezone

from apps.user.models import CustomUser


class OnlineStatusMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            now = timezone.now()
            delta = now - timedelta(minutes=settings.USER_LAST_ACTIVITY_INTERVAL)
            CustomUser.objects.filter(last_activity__lt=delta).update(is_online=False)
            request.user.last_activity = now
            request.user.is_online = True
            request.user.save()

        response = self.get_response(request)
        return response