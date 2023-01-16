from django.apps import AppConfig


class InnoappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'innoapp'

    def ready(self):
        import innoapp.receivers