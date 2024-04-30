from django.db import models
from django.contrib.auth.models import AbstractUser




class User(AbstractUser):
    birthday = models.DateField(null=True)
    image = models.ImageField(null=True)
    point = models.PositiveIntegerField(default=0)
    following = models.ManyToManyField('self',symmetrical=False, related_name="followers", blank=True)
    email = models.EmailField(unique=True)

