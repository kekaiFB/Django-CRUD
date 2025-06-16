from django.apps import AppConfig


class FormulesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'formules'

    def ready(self):
        from django.contrib.auth.models import Group
        Group.objects.get_or_create(name='Врач')
        Group.objects.get_or_create(name='Пациент')
        from . import signals
