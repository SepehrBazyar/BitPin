from django.core.exceptions import ValidationError


def validate_score(value: int):
    """Validate score between 0 and 5

    :param value: integer score number
    :raises ValidationError: if score is invalid
    """
    if not 0 <= value <= 5:
        raise ValidationError(f"Score must be between 0 and 5. Given: {value}")
