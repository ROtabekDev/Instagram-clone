import mimetypes

from django.db import models
from django.conf import settings

from helpers.models import BaseModel, MediaType


class Post(BaseModel):
    """Postlar uchun model"""

    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    description = models.TextField('Tavsif')
    location_id = models.ForeignKey('Location', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Postlar'

    @property
    def comments_count(self):
        return self.comment_set.count()


class PostFileContent(BaseModel):
    """Post uchun content (Video yoki rasm)"""

    CONTENT_TYPE = (
        ('Video', 'Video'),
        ('Rasm', 'Rasm'),
    )

    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    file = models.FileField('Fayl', upload_to='post/post_file_content/file/')
    type = models.CharField(max_length=6, choices=MediaType.choices, default=MediaType.IMG)

    def save(self, *args, **kwargs):
        mime_type, encoding = mimetypes.guess_type(self.file.path)

        if 'video' in mime_type:
            self.content_type = 'Video'
        else:
            self.content_type = 'Rasm'

        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Post uchun kontent'
        verbose_name_plural = 'Post uchun kontentlar'


class Location(BaseModel):
    """Manzil uchun model"""

    name = models.CharField('Manzil nomi', max_length=150)
    longitude = models.DecimalField('Uzunlik', max_digits=9, decimal_places=6, null=True, blank=True)
    latitude = models.DecimalField('Kenglik', max_digits=9, decimal_places=6, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Manzil'
        verbose_name_plural = 'Manzillar'


class Hashtag(BaseModel):
    """Teglar uchun model"""

    tag_name = models.CharField('Nomi', max_length=150)
    slug = models.SlugField('Slugi', max_length=150)

    def __str__(self):
        return self.tag_name

    class Meta:
        verbose_name = 'Teg'
        verbose_name_plural = 'Teglar'


class PostHastag(BaseModel):
    """Postdagi hashteglar uchun model"""
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    tag_id = models.ForeignKey(Hashtag, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Postdagi hashteg'
        verbose_name_plural = 'Postdagi hashteglar'


class SpecifiedUser(BaseModel):
    """Post kontentga belgilangan foydalanuvchilar uchun model"""

    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content_id = models.ForeignKey(PostFileContent, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Belgilangan foydalanuvchi'
        verbose_name_plural = 'Belgilangan foydalanuvchilar'
