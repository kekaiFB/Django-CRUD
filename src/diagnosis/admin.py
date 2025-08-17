
from django.contrib import admin
from django.db.models import ForeignKey, ManyToManyField

class AutoOptimizedAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        select = []
        prefetch = []

        for field in self.model._meta.get_fields():
            if isinstance(field, ForeignKey):
                select.append(field.name)
            elif isinstance(field, ManyToManyField):
                prefetch.append(field.name)

        return qs.select_related(*select).prefetch_related(*prefetch)
    
from django.apps import apps
from django.contrib.admin.sites import AlreadyRegistered

app_config = apps.get_app_config('diagnosis')

for model in app_config.get_models():
    try:
        admin.site.register(model, AutoOptimizedAdmin)
    except AlreadyRegistered:
        pass

