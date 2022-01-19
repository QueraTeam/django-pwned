# Django Pwned

![https://pypi.python.org/pypi/django-pwned/](https://img.shields.io/pypi/v/django-pwned.svg)
![https://github.com/QueraTeam/django-pwned/actions](https://github.com/QueraTeam/django-pwned/workflows/Tests/badge.svg)
![https://github.com/QueraTeam/django-pwned/blob/master/LICENSE.txt](https://img.shields.io/github/license/QueraTeam/django-pwned.svg)
![https://github.com/psf/black](https://img.shields.io/badge/code%20style-black-000000.svg)

A Django password validator using the [Pwned Passwords API] to check for
compromised passwords.

## Installation

For translations to work, add `django_pwned` to `INSTALLED_APPS`.

## Usage

### TL;DR:

```python
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django_pwned.validators.PwnedPasswordValidator"},
    {"NAME": "django_pwned.validators.GitHubLikePasswordValidator"},
]
```

### PwnedPasswordValidator

In `AUTH_PASSWORD_VALIDATORS`, remove `CommonPasswordValidator` and add
`PwnedPasswordValidator`.

Internally, `PwnedPasswordValidator` checks password with Django's
`CommonPasswordValidator` and if password was not in Django's list,
uses Pwned API to check password.

```python
AUTH_PASSWORD_VALIDATORS = [
    # ...
    # {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django_pwned.validators.PwnedPasswordValidator"},
    # ...
]
```

### GitHubLikePasswordValidator

There is also `django_pwned.validators.GitHubLikePasswordValidator` which
checks the password
[is at least](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-strong-password):

- 8 characters long, if it includes a number and a lowercase letter, or
- 15 characters long with any combination of characters

You may want to disable Django's `NumericPasswordValidator`
and `MinimumLengthValidator` if you want to use
`GitHubLikePasswordValidator`.

## Settings

You can set the API request timeout by setting `DJANGO_PWNED_API_REQUEST_TIMEOUT` in
your project settings. (default is 1.5 seconds)

```python
DJANGO_PWNED_API_REQUEST_TIMEOUT = 2.0
```

[pwned passwords api]: https://haveibeenpwned.com/API/v3#PwnedPasswords

## Development

- Create and activate a python virtualenv.
- Install development dependencies in your virtualenv: `pip install -e '.[dev]'`
- Install pre-commit hooks: `pre-commit install`
- Run tests with coverage: `py.test --cov`

## License

MIT
