from django import template
from django.contrib.contenttypes.models import ContentType

from apps.main.models import Like, Comment
from apps.post.models import Post

register = template.Library()


@register.simple_tag
def post_likes_count(post_id):
    content_type = ContentType.objects.get_for_model(Post)
    likes_count = Like.objects.filter(content_type=content_type, object_id=post_id).count()
    return likes_count

# @register.simple_tag
# def post_comments_count(post_id):
#     content_type = ContentType.objects.get_for_model(Comment)
#     comments_count = Comment.objects.filter(content_type=content_type, object_id=post_id).count()
#     return comments_count
