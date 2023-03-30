from django.db import models
from django.contrib.auth.models import AbstractUser

from apps.user.choices import GenderType
from helpers.models import BaseModel, MediaType
from sorl.thumbnail.fields import ImageField
from phonenumber_field.modelfields import PhoneNumberField


class Story(BaseModel):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Story"
        verbose_name_plural = "Stories"


class StoryContent(BaseModel):
    story = models.ForeignKey(Story, on_delete=models.CASCADE)
    file = models.FileField(upload_to="story/%Y/%m/%d/")
    type = models.CharField(max_length=6, choices=MediaType.choices, default=MediaType.IMG)

    def __str__(self):
        return str(self.story.id)

    class Meta:
        verbose_name = "StoryContent"
        verbose_name_plural = "StoryContents"
        