from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
    # UD3.4f - Nombre de la aplicación tal como aparece en el administrador
    verbose_name = 'Monitorización'