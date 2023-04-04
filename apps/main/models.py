from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from helpers.models import BaseModel

from apps.post.models import Post


class Notification(BaseModel):
    """Bildirishnomalar uchun model"""

    NOTIFICATION_TYPE = (
        (1, 'Like'),
        (2, 'Comment'),
        (3, 'Follow')
    )

    sender_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Yuboruvchi user')
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                related_name="notification_from_user", verbose_name='Qabul qiluvchi user')
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="notification_to_user", null=True,
                                blank=True)
    notification_type = models.CharField('Bildirishnoma turi', choices=NOTIFICATION_TYPE, max_length=30, null=True,
                                         blank=True)
    text_preview = models.CharField('Matni', max_length=250)
    viewed = models.BooleanField('Ko`rildi', default=False)

    def __str__(self):
        return self.text_preview[:30]

    class Meta:
        verbose_name = 'Bildirishnoma'
        verbose_name_plural = 'Bildirishnomalar'


class Like(BaseModel):
    """Likelar uchun model"""

    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Foydalanuvchi")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, verbose_name="Model")
    object_id = models.PositiveIntegerField("Obyekt id")
    content_object = GenericForeignKey("content_type", "object_id")

    def __str__(self):
        return f"{self.user_id.first_name} {self.content_object}"

    class Meta:
        verbose_name = 'Like'
        verbose_name_plural = 'Likelar'


class Comment(BaseModel):
    """Izohlar uchun model"""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Muallif')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, verbose_name='Asosiy izoh', blank=True, null=True)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField(verbose_name='Izoh matni')
    is_child = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Izoh'
        verbose_name_plural = 'Izohlar'
