# suscripciones/apps.py

from django.apps import AppConfig

class SuscripcionesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'suscripciones'

    def ready(self):
        import suscripciones.signals  # Importa las señales al iniciar la aplicación
