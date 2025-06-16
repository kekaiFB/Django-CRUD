from django.apps import AppConfig


class DiagnosisConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    # The app directory is named "formules", so Django must know the correct
    # module path. Without this, the application cannot be loaded.
    name = 'formules'

    def ready(self):
        from django.contrib.auth.models import Group
        Group.objects.get_or_create(name='Врач')
        Group.objects.get_or_create(name='Пациент')
        from . import signals
