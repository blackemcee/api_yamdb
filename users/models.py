from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.db.models.enums import TextChoices
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class Roles(TextChoices):
    USER = 'user', 'user'
    MODERATOR = 'moderator', 'moderator'
    ADMIN = 'admin', 'admin'


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True, blank=False)
    is_staff = models.BooleanField(default=True)
    username = models.CharField(
        verbose_name='username',
        blank=True, unique=True, max_length=200
    )
    role = models.CharField(
        max_length=10,
        choices=Roles.choices,
        default=Roles.USER,
    )
    description = models.CharField(
        verbose_name='description',
        blank=True, max_length=200
    )

    bio = models.CharField(
        verbose_name='bio',
        blank=True, max_length=200
    )

    first_name = models.CharField(
        verbose_name='first name',
        blank=True, max_length=200
    )
    last_name = models.CharField(
        verbose_name='last name',
        blank=True, max_length=200
    )
    token = models.CharField(
        verbose_name='token',
        blank=True, max_length=200
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f'{self.email}----{self.username}-----{self.role}'

    class Meta:
        constraints = [
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_role_valid",
                check=models.Q(role__in=Roles.values),
            )
        ]
