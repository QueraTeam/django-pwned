import os

from setuptools import find_packages, setup

from django_pwned import __version__

with open(os.path.join(os.path.dirname(__file__), "README.md"), "r", encoding="UTF-8") as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

dev_requirements = ["pre-commit", "pytest", "pytest-cov", "pytest-django", "responses"]

setup(
    name="django-pwned",
    version=__version__,
    description="A Django password validator using the Pwned Passwords API to check for compromised passwords.",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Mohammad Javad Naderi",
    packages=find_packages(".", include=("django_pwned", "django_pwned.*")),
    include_package_data=True,
    install_requires=["Django>=3.2", "requests"],
    extras_require={"dev": dev_requirements},
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 3.2",
        "Framework :: Django :: 4.0",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Internet :: WWW/HTTP :: Session",
        "Topic :: Security",
    ],
)
