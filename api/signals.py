from django.apps import AppConfig


class SportsappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    def ready(self) -> None:
        import api.signals
