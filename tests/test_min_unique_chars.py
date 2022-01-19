import pytest
from django.core.exceptions import ValidationError

from django_pwned.exceptions import InvalidArgumentsError
from django_pwned.validators import MinimumUniqueCharactersPasswordValidator


def test_default_arguments():
    validator = MinimumUniqueCharactersPasswordValidator()
    with pytest.raises(ValidationError):
        validator.validate("")
    with pytest.raises(ValidationError):
        validator.validate("a12")
    with pytest.raises(ValidationError):
        validator.validate("a12a12a12a12a12a12a12a12a12a12a12a12a12a12a12a12a12a12a12a12a12")
    validator.validate("1a2b")
    validator.validate("aAbB")


def test_invalid_arguments():
    with pytest.raises(InvalidArgumentsError):
        MinimumUniqueCharactersPasswordValidator(min_unique_characters=1)
    MinimumUniqueCharactersPasswordValidator(min_unique_characters=2)


def test_valid_arguments():
    validator = MinimumUniqueCharactersPasswordValidator(min_unique_characters=8)
    with pytest.raises(ValidationError):
        validator.validate("")
    with pytest.raises(ValidationError):
        validator.validate("1a2b3c4")
    with pytest.raises(ValidationError):
        validator.validate("1a2b3c41a2b3c41a2b3c41a2b3c41a2b3c41a2b3c41a2b3c41a2b3c4")
    validator.validate("1a2b3c4d")
    validator.validate("aAbBcCdD")
