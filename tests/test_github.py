import pytest
from django.core.exceptions import ValidationError

from django_pwned.exceptions import InvalidArgumentsError
from django_pwned.validators import GitHubLikePasswordValidator


def test_empty_string():
    validator = GitHubLikePasswordValidator()
    with pytest.raises(ValidationError):
        validator.validate("")

    validator = GitHubLikePasswordValidator(min_length=6, safe_length=7)
    with pytest.raises(ValidationError):
        validator.validate("")


def test_default_arguments():
    validator = GitHubLikePasswordValidator()

    with pytest.raises(ValidationError):
        validator.validate("aaaa777")
    validator.validate("aaaa7777")
    with pytest.raises(ValidationError):
        validator.validate("a" * 8)
    with pytest.raises(ValidationError):
        validator.validate("a" * 14)
    validator.validate("a" * 15)
    validator.validate("a" * 16)


def test_invalid_arguments():
    with pytest.raises(InvalidArgumentsError):
        GitHubLikePasswordValidator(min_length=5, safe_length=15)
    with pytest.raises(InvalidArgumentsError):
        GitHubLikePasswordValidator(min_length=8, safe_length=7)
    with pytest.raises(InvalidArgumentsError):
        GitHubLikePasswordValidator(min_length=8, safe_length=8)
    GitHubLikePasswordValidator(min_length=8, safe_length=9)
    GitHubLikePasswordValidator(min_length=8, safe_length=10)


def test_valid_arguments_1():
    validator = GitHubLikePasswordValidator(min_length=6, safe_length=12)

    with pytest.raises(ValidationError):
        validator.validate("aaa77")
    validator.validate("aaa777")
    with pytest.raises(ValidationError):
        validator.validate("a" * 6)
    with pytest.raises(ValidationError):
        validator.validate("a" * 11)
    validator.validate("a" * 12)
    validator.validate("a" * 13)


def test_valid_arguments_2():
    validator = GitHubLikePasswordValidator(min_length=7, safe_length=8)

    with pytest.raises(ValidationError):
        validator.validate("aaa777")
    validator.validate("aaaa777")
    with pytest.raises(ValidationError):
        validator.validate("a" * 7)
    validator.validate("a" * 8)
    validator.validate("a" * 9)
