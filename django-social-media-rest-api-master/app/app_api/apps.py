from django.apps import AppConfig


class AppApiConfig(AppConfig):
    name = 'app_api'

    def ready(self):
        import app_api.signals

