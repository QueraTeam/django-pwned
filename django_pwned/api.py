"""
Direct access to the Pwned Passwords API for checking whether a password is compromised.
"""

import hashlib
import sys

import requests

from . import __version__

API_ENDPOINT = "https://api.pwnedpasswords.com/range/{}"
USER_AGENT = "django-pwned/{} (Python/{} | requests/{})".format(
    __version__, "{}.{}.{}".format(*sys.version_info[:3]), requests.__version__
)


class PwnedRequestError(Exception):
    pass


def _get_pwned(prefix, request_timeout: float) -> dict[str, int]:
    """
    Fetches a dict of all hash suffixes from Pwned Passwords for a given SHA-1 prefix.
    """
    try:
        response = requests.get(
            url=API_ENDPOINT.format(prefix), headers={"User-Agent": USER_AGENT}, timeout=request_timeout
        )
        response.raise_for_status()
    except requests.RequestException as e:
        raise PwnedRequestError("Error fetching data from Pwned Passwords API: %r" % e)

    results = {}
    for line in response.text.splitlines():
        line_suffix, times = line.split(":", 1)
        results[line_suffix] = int(times.replace(",", ""))

    return results


def get_pwned_count(password: str, request_timeout: float) -> int:
    """
    Checks a password against the Pwned Passwords database.

    Returns an integer (count of how many times the password appears in the Pwned data set)
    Raises PwnedRequestError if it couldn't get response from API (timeout, HTTP error code).
    """
    if not isinstance(password, str):
        raise TypeError("Password values to check must be Unicode strings.")
    password_hash = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
    prefix, suffix = password_hash[:5], password_hash[5:]
    return _get_pwned(prefix, request_timeout).get(suffix, 0)
