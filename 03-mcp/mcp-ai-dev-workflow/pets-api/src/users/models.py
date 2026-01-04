"""
User models for the Petstore API.
"""

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser.
    Adds additional fields required by the Petstore API specification.
    """

    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text="User's phone number"
    )

    user_status = models.IntegerField(
        default=0,
        help_text="User status code (0=active, 1=inactive, etc.)"
    )

    class Meta:
        db_table = "users"
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["-date_joined"]

    def __str__(self):
        return self.username

    def __repr__(self):
        return f"<User {self.username} (id={self.id})>"
