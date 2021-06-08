from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.db.models.enums import TextChoices

from api_yamdb import settings as config
from .managers import CustomUserManager


class Roles(TextChoices):
    USER = 'user', 'user'
    MODERATOR = 'moderator', 'moderator'
    ADMIN = 'admin', 'admin'


class CustomUser(AbstractBaseUser, PermissionsMixin):
    password = models.CharField(
        'password',
        null=True, blank=True, max_length=128
    )

    last_login = None

    email = models.EmailField('email address', unique=True, blank=False)

    is_staff = models.BooleanField(default=True, null=True)
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
        null=True, blank=True, max_length=200
    )

    bio = models.CharField(
        verbose_name='bio',
        null=True,
        blank=True, max_length=200
    )

    first_name = models.CharField(
        verbose_name='first name', null=True,
        blank=True, max_length=200
    )
    last_name = models.CharField(
        verbose_name='last name', null=True,
        blank=True, max_length=200
    )
    confirmation_code = models.CharField(
        verbose_name='confirmation code',
        null=True,
        blank=True, max_length=200
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        ordering = ['username']
        constraints = [
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_role_valid",
                check=models.Q(role__in=Roles.values),
            )
        ]

    def __str__(self):
        return f'{self.email}----{self.username}-----{self.role}'

    @property
    def is_admin(self):
        return self.is_superuser or self.role == config.ADMIN_ROLE

    @property
    def is_moderator(self):
        return self.role == config.MODERATOR_ROLE

    @property
    def is_user(self):
        return self.role == config.USER_ROLE
