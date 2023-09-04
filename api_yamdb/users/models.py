from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _
from users.constants import (EMAIL_MAX_LENGTH, USERS_NAME_MAX_LENGTH, ROLE_MAX_LENGTH, USER, ADMIN, MODERATOR)


class User(AbstractUser):
    """
    Users in the Yamdb authentication system are represented by this
    model.
    """

    class Role(models.TextChoices):
        USER = 'user'
        MODERATOR = 'moderator'
        ADMIN = 'admin'



    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        _("Username"),
        max_length=USERS_NAME_MAX_LENGTH,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. "
            "Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "Unique": _("A user with that username already exists."),
        },
    )
    first_name = models.CharField(
        _("First name"),
        max_length=USERS_NAME_MAX_LENGTH,
        blank=True,
    )
    last_name = models.CharField(
        _("Last name"),
        max_length=USERS_NAME_MAX_LENGTH,
        blank=True,
    )
    email = models.EmailField(
        _("Email address"),
        max_length=EMAIL_MAX_LENGTH,
        unique=True,
    )
    role = models.CharField(
        _("Users role"),
        choices=Role.choices,
        max_length=ROLE_MAX_LENGTH,
        default=USER,
    )
    bio = models.TextField(
        _("Biography"),
        blank=True,
    )

    class Meta:
        ordering = ["id"]
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.role == ADMIN

    @property
    def is_moderator(self):
        return self.role == MODERATOR
