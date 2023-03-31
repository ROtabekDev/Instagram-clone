from django.shortcuts import render
from django.views.generic import TemplateView
from apps.post.models import Post
from .models import Notification


class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.all().exclude(user_id=self.request.user)
        return context


def ShowNotification(request):
    user = request.user
    notifications = Notification.objects.filter(user_id=user).order_by('-created_at')

    context = {
        'notifications': notifications,

    }
    return render(request, 'show-notification.html', context)
