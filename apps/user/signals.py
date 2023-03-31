from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

from .models import UserFollower
from apps.main.models import Notification

@receiver(post_save, sender=UserFollower)
def user_comment_post(sender, instance, created, *args, **kwargs):
    if created:
        follow = instance
        sender = follow.follower
        following = follow.following
        text_preview = f'{following} shu inson sizga obuna bo`ldi' 
        Notification.objects.create(sender_id=sender, user_id=following, text_preview=text_preview, notification_type=3)


@receiver(post_delete, sender=UserFollower)
def user_unfollow(sender, instance, *args, **kwargs):
    follow = instance
    sender = follow.follower
    following = follow.following
    Notification.objects.filter(sender=sender, user=following, notification_type=3).delete() 
 