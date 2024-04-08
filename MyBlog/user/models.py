from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    photo = models.ImageField(upload_to='user_photos/', null=True, blank=True, verbose_name='Фото')
