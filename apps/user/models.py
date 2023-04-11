from django.db import models
from django.contrib.auth.models import AbstractUser

from apps.user.choices import GenderType
from apps.user.custom_user_manager import CustomUserManager
from helpers.models import BaseModel
from sorl.thumbnail.fields import ImageField
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.crypto import get_random_string


class CustomUser(AbstractUser, BaseModel):
    first_name = None
    last_name = None
    full_name = models.CharField(max_length=100)
    avatar = ImageField(null=True, blank=True, upload_to="images/avatar/%Y/%m/%d/")
    birthday = models.DateTimeField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True, unique=True)
    phone_number = PhoneNumberField(region="UZ", null=True, blank=True, unique=True)
    bio = models.CharField(max_length=255, null=True, blank=True)
    gender = models.CharField(max_length=6, choices=GenderType.choices, default=GenderType.MALE)
    last_activity = models.DateTimeField(null=True, blank=True)
    is_online = models.BooleanField(default=False)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["full_name"]

    objects = CustomUserManager()

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

    def save(self, *args, **kwargs):

        if self.full_name=="":
            self.full_name=self.username

        super().save(*args, **kwargs)

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


class Chat(BaseModel):
    name = models.CharField(max_length=200, null=True, blank=True)

    @property
    def un_read(self):
        return self.messages.filter(is_read=False).count()

    @property
    def un_read_obj(self):
        return self.messages.filter(is_read=False)

    def __str__(self):
        return self.name if self.name else ""

    def save(self, *args, **kwargs):
        if self.name is None:
            self.name = get_random_string(17)
        super(Chat, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Chat"
        verbose_name_plural = "Chats"


class Participant(BaseModel):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Participant"
        verbose_name_plural = "Participants"


class Message(BaseModel):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    msg = models.TextField()
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.sender.username

    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"
