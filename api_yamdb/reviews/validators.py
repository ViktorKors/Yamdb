from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
import re


def validate_year(value):
    if value > timezone.now().year:
        raise ValidationError(
            _("The year cannot be %(value)s greater than the current one!"),
            params={"value": value},
        )