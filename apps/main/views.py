from django.shortcuts import render

from django.views.generic import TemplateView
from .models import Notification

class HomeView(TemplateView):
    template_name = "home.html"


def ShowNotification(request):
    user = request.user
    notifications = Notification.objects.filter(user_id=user).order_by('-created_at')

    context = {
        'notifications': notifications,

    }
    return render(request, 'show-notification.html', context)