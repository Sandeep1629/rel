from django.apps import AppConfig


class ResappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'resapp'


class MyAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myapp'

    def ready(self):
        import myapp.signals
