import re

from django.core.exceptions import ValidationError


def only_english_character(value):
    """Validator of model for english characters"""
    try:
        value.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        raise ValidationError(f"This word {value} has not only ascii")
    match = re.findall(r'([a-zA-Z ])', value)
    if len(match) != len(value):
        raise ValidationError(f"This word {value} has not english character")


def only_russian_character(value):
    """Validator of model for russian characters"""
    match = re.findall(r'([а-яА-Я Ё])', value)
    if len(match) != len(value):
        raise ValidationError(f"This word {value} has not russian character")