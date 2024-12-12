import uuid
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    groups = models.ManyToManyField(
        Group,
        related_name="customuser_set",  # Avoid clashes with auth.User.groups
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="customuser_set",  # Avoid clashes with auth.User.user_permissions
        blank=True,
    )

    def __str__(self):
        return self.username
