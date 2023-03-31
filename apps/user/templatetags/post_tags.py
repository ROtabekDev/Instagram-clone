from django import template
from django.contrib.contenttypes.models import ContentType

from apps.main.models import Like, Comment
from apps.post.models import Post
import datetime

register = template.Library()


@register.simple_tag
def post_likes_count(post_id):
    content_type = ContentType.objects.get_for_model(Post)
    likes_count = Like.objects.filter(content_type=content_type, object_id=post_id).count()
    text = f'{likes_count} like' if likes_count < 2 else f'{likes_count} <a class="post__name--underline">likes</a>'
    return text


@register.simple_tag
def post_time_delta(created_at):
    created_at = created_at.strftime("%Y-%m-%d %H:%M:%S")
    created_at = datetime.datetime.strptime(created_at, '%Y-%m-%d %H:%M:%S')

    now = datetime.datetime.now()
    time_diff = now - created_at
    hour = time_diff.seconds // 3600
    if hour < 1:
        minute = time_diff.seconds // 60
        if minute < 2:
            text = f'{minute} minute'
        else:
            text = f'{minute} minutes'
    else:
        if hour >= 24:
            day = hour // 24
            if day < 2:
                text = f'{day} day'
            else:
                text = f'{day} days'
        else:
            if hour < 2:
                text = f'{hour} hour'
            else:
                text = f'{hour} hours'
    return text
