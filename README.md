Django Pwned
============

A Django password validator using the [Pwned Passwords API] to check for
compromised passwords.

## Installation

For translations to work, add `django_pwned` to `INSTALLED_APPS`.

## Usage

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

There is also `django_pwned.validators.GitHubLikePasswordValidator` which
checks the password
[is at least](https://docs.github.com/en/github/authenticating-to-github/creating-a-strong-password):

- 8 characters long, if it includes a number and a lowercase letter, or
- 15 characters long with any combination of characters

You may want to disable Django's `NumericPasswordValidator`
and `MinimumLengthValidator` if you want to use
`GitHubLikePasswordValidator`.

Example validators:

```python
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django_pwned.validators.PwnedPasswordValidator"},
    {"NAME": "django_pwned.validators.GitHubLikePasswordValidator"},
]
```

## Settings

You can set the API request timeout by setting `PWNED_API_REQUEST_TIMEOUT` in
your project settings. (default is 1.5 seconds)

```python
PWNED_API_REQUEST_TIMEOUT = 2.0 
```

[Pwned Passwords API]: https://haveibeenpwned.com/API/v3#PwnedPasswords
