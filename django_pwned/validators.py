"""
A Django password validator using the Pwned Passwords API to check for
compromised passwords.
"""

from django.contrib.auth.password_validation import CommonPasswordValidator
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _

from . import api

common_password_validator = CommonPasswordValidator()


@deconstructible
class PwnedPasswordValidator:
    """
    Password validator which checks Django's list of common passwords and the Pwned Passwords database.
    """

    def validate(self, password: str, user=None):
        # First, check Django's list of common passwords
        common_password_validator.validate(password, user)

        # If password is not in Django's list, check Pwned API
        count = api.get_pwned_count(password)
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
