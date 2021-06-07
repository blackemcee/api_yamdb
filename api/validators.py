from datetime import datetime

from django.core.exceptions import ValidationError


def title_year_validator(value):
    if value > datetime.now().year:
        raise ValidationError(
            "Year can't be in the future",
            params={'value': value},
        )
