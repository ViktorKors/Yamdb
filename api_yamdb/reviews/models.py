from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Genre(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _("Genre")
        verbose_name_plural = _("Genres")


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")


class Titles(models.Model):
    name = models.CharField(verbose_name=_("Name"), max_length=100)
    year = models.IntegerField()
    description = models.TextField()
    genre = models.ManyToManyField(Genre, through="GenreTitles")
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="category",
    )
    rating = models.IntegerField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Title")
        verbose_name_plural = _("Titles")


class GenreTitles(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    titles = models.ForeignKey(Titles, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.genre} {self.titles}"

    class Meta:
        verbose_name = _("Genre and Title")
        verbose_name_plural = _("Genres and Titles")


class Reviews(models.Model):
    text = models.CharField(verbose_name=_("Text"), max_length=100)
    title = models.ForeignKey(
        Titles,
        verbose_name=_("Title"),
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        User,
        verbose_name=_("Author"),
        on_delete=models.CASCADE,
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Publication date"),
    )

    class Meta:
        verbose_name = _("Review")
        verbose_name_plural = _("Reviews")


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        verbose_name=_("Author"),
        on_delete=models.CASCADE,
    )
    text = models.CharField(
        verbose_name=_("Commets text"),
        max_length=256,
    )
    review = models.ForeignKey(
        Reviews,
        verbose_name=_("Review"),
        on_delete=models.CASCADE,
        related_name="comments",
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created"),
    )

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")


