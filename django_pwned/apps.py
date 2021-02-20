from django.apps import AppConfig


class DjangoPwnedConfig(AppConfig):
    name = "django_pwned"
    verbose_name = "Django Pwned"

    def ready(self):
        pass
