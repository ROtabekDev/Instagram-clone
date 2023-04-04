from django.contrib.auth.models import BaseUserManager
from django.utils import timezone
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, username=None, email=None, phone_number=None, password=None, **extra_fields):
        if not (email or phone_number or username):
            raise ValueError('At least one of email, phone_number, or username must be set')

        now = timezone.now()

        user = self.model(
            username=username,
            email=self.normalize_email(email) if email else None,
            phone_number=phone_number,
            last_login=now,
            date_joined=now,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username=None, email=None, phone_number=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not extra_fields.get('is_staff'):
            raise ValueError('Superuser must have is_staff=True')
        if not extra_fields.get('is_superuser'):
            raise ValueError('Superuser must have is_superuser=True')

        return self.create_user(
            username=username,
            email=email,
            phone_number=phone_number,
            password=password,
            **extra_fields
        )

    def get_by_natural_key(self, username):
        return self.get(
            models.Q(username__iexact=username) |
            models.Q(email__iexact=username) |
            models.Q(phone_number__iexact=username)
        )
