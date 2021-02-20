Django Pwned
============

A Django password validator using the [Pwned Passwords API] to check for
compromised passwords.

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

## Settings

You can set the api request timeout by setting `PWNED_API_REQUEST_TIMEOUT` in
your project settings. (default is 1.5 seconds)

```python
PWNED_API_REQUEST_TIMEOUT = 2.0 
```

[Pwned Passwords API]: https://haveibeenpwned.com/API/v3#PwnedPasswords
