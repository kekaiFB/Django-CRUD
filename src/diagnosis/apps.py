from django.apps import AppConfig

class DiagnosisConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'diagnosis'

    def ready(self):
        from . import signals  # ✅ Только импорт сигналов
