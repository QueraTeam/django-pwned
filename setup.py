import os
from django_pwned import __version__
from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), "README.md"), "r", encoding="UTF-8") as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name="django-pwned",
    version=__version__,
    description="A Django password validator using the Pwned Passwords API to check for compromised passwords.",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Mohammad Javad Naderi",
    packages=find_packages(".", include=("django_pwned", "django_pwned.*")),
    include_package_data=True,
    install_requires=["Django>=3.1", "requests"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 3.1",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.9",
        "Topic :: Internet :: WWW/HTTP :: Session",
        "Topic :: Security",
    ],
)
