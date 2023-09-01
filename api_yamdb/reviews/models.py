from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from .validators import validate_year

NAME_MAX_LENGTH = 100
SLUG_MAX_LENGTH = 50
EMAIL_MAX_LENGTH = 254
USERS_NAME_MAX_LENGTH = 150
ROLE_MAX_LENGTH = 50
MINVALUE = 1
MAXVALUE = 10
MIN_MAX_VALUE = _("Enter a value from 1 to 10")


class User(AbstractUser):
    """
    Users in the Yamdb authentication system are represented by this
    model.
    """

    USER = "user"
    ADMIN = "admin"
    MODERATOR = "moderator"
    ROLES = [
        (USER, _("Authenticated user")),
        (MODERATOR, _("Moderator")),
        (ADMIN, _("Administrator")),
    ]
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
        choices=ROLES,
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
        return self.role == self.ADMIN

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR


class Category(models.Model):
    """Category model."""

    name = models.CharField(
        _("Name of category"),
        max_length=NAME_MAX_LENGTH,
    )
    slug = models.SlugField(
        _("Category slug"),
        unique=True,
        max_length=SLUG_MAX_LENGTH,
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")


class Genre(models.Model):
    """Work genre model."""

    name = models.CharField(
        _("Genres name"),
        max_length=NAME_MAX_LENGTH,
    )
    slug = models.SlugField(
        _("Genres slug"),
        unique=True,
        max_length=SLUG_MAX_LENGTH,
    )

    class Meta:
        ordering = ["name"]
        verbose_name = _("Genre")
        verbose_name_plural = _("Genres")

    def __str__(self):
        return self.name


class Title(models.Model):
    """Title model."""

    name = models.CharField(
        _("Name"),
        max_length=NAME_MAX_LENGTH,
    )
    year = models.IntegerField(_("Year"), validators=(validate_year,))
    description = models.TextField(
        _("Description"),
        null=True,
        blank=True,
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name=_("Genres"),
        related_name="titles",
        blank=True,
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name="titles",
        verbose_name=_("Category"),
        null=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = _("Title")
        verbose_name_plural = _("Titles")


class GenreTitle(models.Model):
    """Model that connects genres and titles."""

    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)


class Review(models.Model):
    """Artwork review model."""

    text = models.TextField(
        _("Text"),
    )
    pub_date = models.DateTimeField(
        _("Publication date"), auto_now_add=True, db_index=True
    )
    score = models.PositiveSmallIntegerField(
        _("Feedback score"),
        validators=[
            MinValueValidator(MINVALUE, MIN_MAX_VALUE),
            MaxValueValidator(MAXVALUE, MIN_MAX_VALUE),
        ],
    )
    title = models.ForeignKey(
        Title,
        verbose_name=_("Title"),
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    author = models.ForeignKey(
        User,
        verbose_name=_("Author"),
        on_delete=models.CASCADE,
        related_name="reviews",
    )

    class Meta:
        ordering = ("-pub_date",)
        constraints = [
            models.UniqueConstraint(
                fields=["title", "author"], name="unique_review"
            ),
        ]
        verbose_name = _("Review")
        verbose_name_plural = _("Reviews")


class Comment(models.Model):
    """Comment model."""

    author = models.ForeignKey(
        User,
        verbose_name=_("Author"),
        on_delete=models.CASCADE,
        related_name="comments",
    )
    text = models.TextField(
        _("Comments text"),
    )
    review = models.ForeignKey(
        Review,
        verbose_name=_("Review"),
        on_delete=models.CASCADE,
        related_name="comments",
    )
    pub_date = models.DateTimeField(
        _("Publication date"),
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        ordering = [
            "-pub_date",
        ]
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")

    def __str__(self):
        return self.text
