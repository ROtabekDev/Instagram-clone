from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

from .models import Comment, Like, Notification
from apps.post.models import Post

@receiver(post_save, sender=Comment)
def user_comment_post(sender, instance, created, *args, **kwargs):
    if created:
        comment = instance
        if comment.parent: 
            text_preview = f'{comment.user} shu inson sizning {post.id}-postdagi izohingizga javob yozdi.'
        else:
            text_preview = f'{comment.user} shu inson sizning {post.id}-postingizga izoh yozdi.'

        post = comment.post_id 
        sender = comment.user
        Notification.objects.create(post_id=post, sender_id=sender, user_id=post.user_id, text_preview=text_preview, notification_type=2)
        

@receiver(post_delete, sender=Comment)
def user_del_comment_post(sender, instance, *args, **kwargs):
    comment = instance
    post = comment.post_id
    sender = comment.user
    notify = Notification.objects.filter(post_id=post, sender_id=sender, user_id=post.user_id, notification_type=2)[0]
    notify.delete()


@receiver(post_save, sender=Like)
def user_liked_post(sender, instance, created, *args, **kwargs):
    if created:
        like = instance 
        if like.content_type.model=='post': # content_type==12 - post
            post = Post.objects.filter(id=like.object_id)[0]
            sender = like.user_id
            text_preview = f'{like.user_id} shu inson sizning {post.id}-postingizga like bosdi.'
            Notification.objects.create(post_id=post, sender_id=sender, user_id=post.user_id, text_preview=text_preview, notification_type=1)
        elif like.content_type.model=='comment': # content_type==12 - comment
            comment = Comment.objects.filter(id=like.object_id)[0]
            sender = like.user_id
            text_preview = f'{like.user_id} shu inson sizning {comment.post_id} shu postga qoldirgan kommentingizga like bosdi.'
            Notification.objects.create(comment_id=comment, sender_id=sender, user_id=comment.user, text_preview=text_preview, notification_type=1)
    

@receiver(post_delete, sender=Like)
def user_unliked_post(sender, instance, *args, **kwargs): 
    like = instance
    if like.content_type.model=='post': # content_type==12 - post
        post = Post.objects.filter(id=like.object_id)[0]
        sender = like.user_id 
        Notification.objects.filter(post_id=post, sender_id=sender, user_id=post.user_id, notification_type=1).delete()
    elif like.content_type.model=='comment': # content_type==12 - comment
        comment = Comment.objects.filter(id=like.object_id)[0]
        sender = like.user_id 
        Notification.objects.filter(comment_id=comment, sender_id=sender, user_id=comment.user, notification_type=1).delete()
