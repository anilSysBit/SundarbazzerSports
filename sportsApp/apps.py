from django.apps import AppConfig


class SportsappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sportsApp'

    def ready(self) -> None:
        import sportsApp.signals
