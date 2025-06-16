from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ('formules', '0003_create_superuser'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='formules',
            name='pol',
        ),
        migrations.RemoveField(
            model_name='formules',
            name='vozrast',
        ),
        migrations.RemoveField(
            model_name='formules',
            name='ves',
        ),
        migrations.RemoveField(
            model_name='formules',
            name='rost',
        ),
    ]
