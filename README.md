# Django Pwned

[![](https://img.shields.io/pypi/v/django-pwned.svg)](https://pypi.python.org/pypi/django-pwned/)
[![](https://github.com/QueraTeam/django-pwned/workflows/Tests/badge.svg)](https://github.com/QueraTeam/django-pwned/actions)
[![](https://img.shields.io/github/license/QueraTeam/django-pwned.svg)](https://github.com/QueraTeam/django-pwned/blob/master/LICENSE.txt)
[![](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A collection of django password validators.

## Compatibility

- Python: **3.6**, **3.7**, **3.8**, **3.9**, **3.10**
- Django: **3.2**, **4.0**

## Installation

```
pip install django-pwned
```

For translations to work, add `django_pwned` to `INSTALLED_APPS`.

## TL;DR:

```python
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django_pwned.validators.GitHubLikePasswordValidator"},
    {"NAME": "django_pwned.validators.MinimumUniqueCharactersPasswordValidator"},
    {"NAME": "django_pwned.validators.PwnedPasswordValidator"},
]
```

## Validators

### PwnedPasswordValidator(request_timeout=1.5)

This validator uses the [Pwned Passwords API] to check for compromised passwords.

Internally, this validator checks password with django's
`CommonPasswordValidator` and if password was not in django's list,
uses Pwned API to check password. So you can remove `CommonPasswordValidator`
if you're using this validator.

```python
AUTH_PASSWORD_VALIDATORS = [
    # ...
    # {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django_pwned.validators.PwnedPasswordValidator"},
    # ...
]
```

You can set the API request timeout with the `request_timeout` parameter (in seconds).

If for any reason (connection issues, timeout, ...) the request to Pwned API fails,
this validator skips checking password.

### GitHubLikePasswordValidator(min_length=8, safe_length=15)

Validates whether the password is at least:

- 8 characters long, if it includes a number and a lowercase letter, or
- 15 characters long with any combination of characters

Based on Github's documentation about [creating a strong password].

You may want to disable Django's `NumericPasswordValidator`
and `MinimumLengthValidator` if you want to use
`GitHubLikePasswordValidator`.

The minimum number of characters can be customized with the `min_length`
parameter. The length at which we remove the restriction about
requiring both number and lowercase letter can be customized with the
`safe_length` parameter.

### MinimumUniqueCharactersPasswordValidator(min_unique_characters=4)

Validates whether the password contains at least 4 unique characters.
For example `aaaaaaaaaabbbbbbccc` is an invalid password, but `aAbB` is a valid password.

The minimum number of unique characters can be customized with the
`min_unique_characters` parameter.

## Development

- Create and activate a python virtualenv.
- Install development dependencies in your virtualenv: `pip install -e '.[dev]'`
- Install pre-commit hooks: `pre-commit install`
- Run tests with coverage: `py.test --cov`

## License

MIT

[pwned passwords api]: https://haveibeenpwned.com/API/v3#PwnedPasswords
[creating a strong password]: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-strong-password
