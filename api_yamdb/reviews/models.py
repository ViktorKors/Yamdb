from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Titles(models.Model):
    pass


class Reviews(models.Model):
    text = models.CharField(verbose_name=_("Text"))
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
