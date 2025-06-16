from django.db import migrations
from django.contrib.auth import get_user_model


def create_superuser(apps, schema_editor):
    User = get_user_model()
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(username='admin', password='admin', email='admin@example.com')


def remove_superuser(apps, schema_editor):
    User = get_user_model()
    User.objects.filter(username='admin').delete()


class Migration(migrations.Migration):
    dependencies = [
        ('formules', '0002_formules_patient'),
    ]

    operations = [
        migrations.RunPython(create_superuser, remove_superuser),
    ]
