from django.db import migrations, models
from django.conf import settings

class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Diagnosis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('simptomy_dni', models.IntegerField(blank=True, null=True, verbose_name='Начало или длительность симптомов (в днях)')),
                ('anamnez', models.IntegerField(blank=True, null=True, verbose_name='Анамнез')),
                ('kashel', models.IntegerField(blank=True, null=True, verbose_name='Кашель')),
                ('mokrota', models.IntegerField(blank=True, null=True, verbose_name='Мокрота')),
                ('odyshka', models.IntegerField(blank=True, null=True, verbose_name='Отдышка')),
                ('temperatura', models.FloatField(blank=True, null=True, verbose_name='Температура тела')),
                ('pritplenie', models.IntegerField(blank=True, null=True, verbose_name='Притупление перкуторного звука')),
                ('oslablenie', models.IntegerField(blank=True, null=True, verbose_name='Ослабление везикулярного дыхания')),
                ('auskultaciya', models.IntegerField(blank=True, null=True, verbose_name='Аускультативная картина')),
                ('saturaciya', models.FloatField(blank=True, null=True, verbose_name='Уровень сатурации О2')),
                ('chss', models.IntegerField(blank=True, null=True, verbose_name='Частота сокращений')),
                ('ofv1', models.FloatField(blank=True, null=True, verbose_name='ОФВ1')),
                ('zhel_ofv1', models.FloatField(blank=True, null=True, verbose_name='ЖЕЛ, ОФВ1')),
                ('limfadenopatiya', models.IntegerField(blank=True, null=True, verbose_name='Лимфаденопатия')),
                ('ochagi', models.IntegerField(blank=True, null=True, verbose_name='Очаги')),
                ('konsolidacii', models.IntegerField(blank=True, null=True, verbose_name='Консолидации')),
                ('fibrozno_kistoznye', models.IntegerField(blank=True, null=True, verbose_name='Фиброзно-кистозные изменения')),
                ('polosti', models.IntegerField(blank=True, null=True, verbose_name='Полости')),
                ('fibroz', models.IntegerField(blank=True, null=True, verbose_name='Фиброз')),
                ('plevralnyj_vypot', models.IntegerField(blank=True, null=True, verbose_name='Плевральный выпот')),
                ('leykocity', models.FloatField(blank=True, null=True, verbose_name='Лейкоциты, х10^9')),
                ('palochko', models.FloatField(blank=True, null=True, verbose_name='Палочкоядерные, %')),
                ('eozinofily', models.FloatField(blank=True, null=True, verbose_name='Эозинофилы, %')),
                ('soe', models.FloatField(blank=True, null=True, verbose_name='СОЭ мм/ч')),
                ('bak_srb', models.FloatField(blank=True, null=True, verbose_name='БАК (СРБ, мг/л)')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата редактирования')),
                ('imt', models.FloatField(blank=True, null=True, verbose_name='ИМТ')),
                ('patient', models.ForeignKey(blank=True, null=True, on_delete=models.SET_NULL, related_name='diagnosis', to=settings.AUTH_USER_MODEL, verbose_name='Пациент')),
            ],
            options={
                'verbose_name_plural': 'Формулы',
            },
        ),
    ]
