from django.apps import AppConfig


class AformAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'aform_app'

    def ready(self):
        import aform_app.signals
