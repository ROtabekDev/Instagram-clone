from django.db import models
from django.contrib.auth.models import AbstractUser

from apps.user.choices import GenderType
from helpers.models import BaseModel
from sorl.thumbnail.fields import ImageField
from phonenumber_field.modelfields import PhoneNumberField


class CustomUser(AbstractUser, BaseModel):
    first_name = None
    last_name = None
    full_name = models.CharField(max_length=100)
    avatar = ImageField(null=True, blank=True, upload_to="images/avatar/%Y/%m/%d/")
    birthday = models.DateTimeField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone_number = PhoneNumberField(region="UZ", null=True, blank=True)
    bio = models.CharField(max_length=255, null=True, blank=True)
    gender = models.CharField(max_length=6, choices=GenderType.choices, default=GenderType.MALE)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.username

    @classmethod
    def is_phone_number_available(cls, phone_number):
        if cls.objects.filter(phone_number=phone_number).exists():
            return False
        return True

    @classmethod
    def is_email_available(cls, email):
        if cls.objects.filter(email=email).exists():
            return False
        return True


class UserFollower(BaseModel):
    follower = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='follower')
    following = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='following')

    def __str__(self):
        return f"{self.follower} follows to {self.following}"

    class Meta:
        verbose_name = "UserFollower"
        verbose_name_plural = "UserFollowers"


class HashTag(BaseModel):
    name = models.CharField(max_length=50)
    avatar = ImageField(null=True, blank=True, upload_to="images/avatar/%Y/%m/%d/")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "HashTag"
        verbose_name_plural = "HashTags"


class HashTagFollower(BaseModel):
    follower = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    hashtag = models.ForeignKey(HashTag, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.follower} follows to {self.hashtag}"

    class Meta:
        verbose_name = "HashTagFollower"
        verbose_name_plural = "HashTagFollowers"