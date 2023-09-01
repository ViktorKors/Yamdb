from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


def validate_year(value):
    """
    The function checks that it is not possible to set the next year.
    """
    if value > timezone.now().year:
        raise ValidationError(
            _("The year cannot be %(value)s greater than the current one!"),
            params={"value": value},
        )
