import json

from django.views.generic import TemplateView
from django.http import JsonResponse

from apps.main.models import Comment
from apps.post.models import Post


class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.filter(user_id__following__follower=self.request.user).exclude(
            user_id=self.request.user)
        return context


def add_comment(request):
    data = json.loads(request.body)
    post_id = data['post_id']
    comment = data['comment']
    comment = Comment.objects.create(user=request.user, post_id_id=post_id, text=comment)
    data = {
        "post_id": comment.post_id_id,
        "user": comment.user.username,
        "comment": comment.text
    }
    return JsonResponse(data)
