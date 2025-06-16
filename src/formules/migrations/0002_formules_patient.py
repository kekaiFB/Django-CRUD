from django.db import migrations, models
from django.conf import settings

class Migration(migrations.Migration):

    dependencies = [
        ('formules', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='formules',
            name='patient',
            field=models.ForeignKey(blank=True, null=True, on_delete=models.SET_NULL, related_name='formules', to=settings.AUTH_USER_MODEL, verbose_name='Пациент'),
        ),
    ]

