from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # Добавьте параметр related_name к полям groups и user_permissions
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',  # Убедитесь, что это уникально
        blank=True,
        help_text=('The groups this user belongs to. A user will get all permissions '
                   'granted to each of their groups.'),
        verbose_name=('groups'),
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',  # Убедитесь, что это уникально
        blank=True,
        help_text=('Specific permissions for this user.'),
        verbose_name=('user permissions'),
    )

    user_address = models.CharField(max_length=128, null=True, blank=True)
    email = models.EmailField(unique=True)
