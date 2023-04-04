from django.utils import timezone
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

from apps.post.models import Post 
from apps.user.models import CustomUser
from .models import Story, StoryContent, StoryViewed


class Stories_detail(TemplateView):
    template_name = "stories_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        stories = Story.objects.filter(
            created_at__gte=timezone.now() - timezone.timedelta(hours=24)
        ).filter(user_id__username=kwargs['username'])

        context['stories'] = stories 
        for story in stories:
            StoryViewed.objects.update_or_create(story=story, user_id=self.request.user)
        return context
    
