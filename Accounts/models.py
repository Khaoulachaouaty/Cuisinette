from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission



class User(AbstractUser):
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)  # Ajout du champ
    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',  # Utilisez un `related_name` unique
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_permissions_set',  # Utilisez un `related_name` unique
        blank=True,
    )

