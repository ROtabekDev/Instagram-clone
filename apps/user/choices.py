from django.db import models


class GenderType(models.TextChoices):
    MALE = "Male"
    FEMALE = "Female"
