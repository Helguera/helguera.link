"""
Database models
"""
import string
import random

from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)

class UserManager(BaseUserManager):
    """Manager for users"""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user"""
        if not email:
            raise ValueError('User must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_superuser(self, email, password):
        """Create and return a new superuser"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user

class User(AbstractBaseUser, PermissionsMixin):
    """User in the system"""
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Link(models.Model):
    """Link objects"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    original_url = models.URLField(max_length=500)
    short_url = models.CharField(max_length=500, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    times_accessed = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        """Custom save method"""
        if not self.short_url:
            self.short_url = self._generate_unique_short_url()
        super().save(*args, **kwargs)

    def _generate_unique_short_url(self):
        length = 3  
        chars = string.ascii_letters + string.digits
        while True:
            new_short_url = ''.join(random.choices(chars, k=length))
            if not Link.objects.filter(short_url=new_short_url).exists():
                return new_short_url

    def __str__(self):
        return self.short_url

