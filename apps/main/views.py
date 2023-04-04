import json
from django.utils import timezone
from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.db.models import Count

from apps.main.models import Comment, Notification, Like
from apps.post.models import Post, SavedPost
from apps.story.models import Story, StoryViewed
 
from apps.user.models import UserFollower, CustomUser
 
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
 


@method_decorator(login_required, name='dispatch')
class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = Post.objects.filter(user_id__following__follower=self.request.user).exclude(
            user_id=self.request.user)
        context['posts'] = posts 
        
        unfollow_users = CustomUser.objects.all().exclude(following__follower=self.request.user).exclude(
            id=self.request.user.id)
        context['unfollow_users'] = unfollow_users

        follow_users = CustomUser.objects.all().filter(following__follower=self.request.user).exclude(
            id=self.request.user.id)
        context['follow_users'] = follow_users
        

        likes = Like.objects.filter(user_id=self.request.user).filter(content_type__model='post').values_list('object_id', flat=True).order_by('object_id')
        if likes.exists():
            context['like_indexes'] = list(likes)
        else:
            context['like_indexes'] = []

        saved_posts = SavedPost.objects.filter(user_id=self.request.user).values_list('post_id', flat=True).order_by('post_id')
        
        if saved_posts.exists():
            context['saved_posts'] = list(saved_posts)
        else:
            context['saved_posts'] = []

        context['no_posts'] = posts.exists()

        stories = Story.objects.filter(user_id__following__follower=self.request.user).exclude(
            user_id=self.request.user).filter(
            created_at__gte=timezone.now() - timezone.timedelta(hours=24)
        )
        
        user_id = Story.objects.filter(user_id__following__follower=self.request.user).exclude(
            user_id=self.request.user).filter(
            created_at__gte=timezone.now() - timezone.timedelta(hours=24)
        ).values_list('user', flat=True).order_by('-created_at')
        
        user_id_list = list(set(user_id)) 
      
        story_info = {}
        
        for j in user_id_list:
            if len(stories.filter(user_id=j))==1:
                try:
                    for i in stories.filter(user_id=j):
                        story = Story.objects.get(user_id=j)
                        StoryViewed.objects.get(user_id=self.request.user, story=story)

                    story_info[j] = {'user_id': j, 'message': True}
                except: 
                    story_info[j] = {'user_id': j, 'message': False}
            else:
                try:
                    user_stories = Story.objects.filter(user_id=j)
                    for i in user_stories: 
                        StoryViewed.objects.get(user_id=self.request.user, story=i)

                    story_info[j] = {'user_id': j, 'message': True}
                except:
                    
                    story_info[j] = {'user_id': j, 'message': False}
                 
        context['story_info'] = story_info
        context['user_id_list'] = user_id_list 

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

@login_required(login_url='sign-in')
def ShowNotification(request):
    user = request.user
    notifications = Notification.objects.filter(user_id=user).order_by('-created_at')

    context = {
        'notifications': notifications,
    }
    notifications = Notification.objects.filter(user_id=user)
    
    for notification in notifications:
        notification.viewed = True
        notification.save()

    return render(request, 'show-notification.html', context)
