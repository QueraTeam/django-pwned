"""
A Django password validator using the Pwned Passwords API to check for
compromised passwords.
"""
import string

from django.contrib.auth.password_validation import CommonPasswordValidator, MinimumLengthValidator
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _

from django_pwned.exceptions import InvalidArgumentsError

from . import api

common_password_validator = CommonPasswordValidator()


@deconstructible
class PwnedPasswordValidator:
    """
    Password validator which checks Django's list of common passwords and the Pwned Passwords database.
    """

    def __init__(self, request_timeout=1.5):
        self.request_timeout = request_timeout

    def validate(self, password: str, user=None):
        # First, check Django's list of common passwords
        common_password_validator.validate(password, user)

        # If password is not in Django's list, check Pwned API
        count = api.get_pwned_count(password, self.request_timeout)
        if count is None:
            # API failure.
            pass
        if count:
            raise ValidationError(
                _("Password is in a list of passwords commonly used on other websites."),
                code="password_pwned",
            )

    def get_help_text(self):
        return _("Your password can’t be in the list of commonly used passwords on other websites.")


class GitHubLikePasswordValidator:
    """
    Implements this rule by GitHub:

    Make sure password is at least 15 characters OR at least 8 characters including a number and a lowercase letter.
    """

    def __init__(self, min_length=8, safe_length=15):
        if min_length < 6:
            raise InvalidArgumentsError("min_length must be at least 6")
        if safe_length <= min_length:
            raise InvalidArgumentsError("safe_length must be greater than min_length")
        self.min_length_validator = MinimumLengthValidator(min_length=min_length)
        self.safe_length = safe_length

    def validate(self, password, user=None):
        self.min_length_validator.validate(password, user)
        # password is at least "min_length" characters
        if len(password) >= self.safe_length:
            # password is at least "safe_length" characters
            return
        if len(set(password) & set(string.ascii_lowercase)) > 0 and len(set(password) & set(string.digits)) > 0:
            # password includes a number and a lowercase letter
            return
        raise ValidationError(
            _("Passwords shorter than %(safe_length)d characters must include a number and a lowercase letter.")
            % {"safe_length": self.safe_length},
            code="password_github_like_validator",
        )


class MinimumUniqueCharactersPasswordValidator:
    """
    Make sure password contains at least 4 unique characters
    """

    def __init__(self, min_unique_characters=4):
        if min_unique_characters < 2:
            raise InvalidArgumentsError("min_unique_characters must be at least 2")
        self.min_unique_characters = min_unique_characters

    def validate(self, password, user=None):
        if len(set(password)) >= self.min_unique_characters:
            # password has at least "min_unique_characters" unique characters
            return
        raise ValidationError(
            _("Make sure password has at least %(min_unique_characters)d unique characters.")
            % {"min_unique_characters": self.min_unique_characters},
            code="password_min_unique_characters_validator",
        )
