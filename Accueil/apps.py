from django.apps import AppConfig


class AccueilConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Accueil'

    def ready(self):
        import Accueil.signals 