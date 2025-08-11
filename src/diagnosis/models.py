from django.db import models
from django.conf import settings
"""Database models for the diagnosis app."""

class Diagnosis(models.Model):
    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="diagnosis",
        verbose_name="Пациент",
        blank=True,
        null=True,
    )

    diagnosis = models.CharField("Диагноз", max_length=255, blank=True, null=True)

    simptomy_dni = models.IntegerField("Начало или длительность симптомов (в днях)", blank=True, null=True)
    anamnez = models.IntegerField("Анамнез", blank=True, null=True)
    kashel = models.IntegerField("Кашель", blank=True, null=True)
    mokrota = models.IntegerField("Мокрота", blank=True, null=True)
    odyshka = models.IntegerField("Отдышка", blank=True, null=True)
    temperatura = models.FloatField("Температура тела", blank=True, null=True)
    pritplenie = models.IntegerField("Притупление перкуторного звука", blank=True, null=True)
    oslablenie = models.IntegerField("Ослабление везикулярного дыхания", blank=True, null=True)
    vlazhnye_hripi = models.IntegerField("Влажные хрипы", blank=True, null=True)
    krepitaciya = models.IntegerField("Крепитация", blank=True, null=True)
    suhie_hripi = models.IntegerField("Сухие хрипы", blank=True, null=True)
    distancnye_svistyashchie_hripi = models.IntegerField("Дистантные свистящие хрипы", blank=True, null=True)
    auskultaciya = models.IntegerField("Аускультативная картина", blank=True, null=True)
    saturaciya = models.FloatField("Уровень сатурации О2", blank=True, null=True)
    chss = models.IntegerField("Частота сокращений", blank=True, null=True)
    ofv1 = models.FloatField("ОФВ1", blank=True, null=True)
    zhel_ofv1 = models.FloatField("ЖЕЛ, ОФВ1", blank=True, null=True)
    limfadenopatiya = models.IntegerField("Лимфаденопатия", blank=True, null=True)
    ochagi = models.IntegerField("Очаги", blank=True, null=True)
    konsolidacii = models.IntegerField("Консолидации", blank=True, null=True)
    fibrozno_kistoznye = models.IntegerField("Фиброзно-кистозные изменения", blank=True, null=True)
    polosti = models.IntegerField("Полости", blank=True, null=True)
    fibroz = models.IntegerField("Фиброз", blank=True, null=True)
    plevralnyj_vypot = models.IntegerField("Плевральный выпот", blank=True, null=True)
    leykocity = models.FloatField("Лейкоциты, х10^9", blank=True, null=True)
    palochko = models.FloatField("Палочкоядерные, %", blank=True, null=True)
    eozinofily = models.FloatField("Эозинофилы, %", blank=True, null=True)
    soe = models.FloatField("СОЭ мм/ч", blank=True, null=True)
    bak_srb = models.FloatField("БАК (СРБ, мг/л)", blank=True, null=True)

    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    updated_at = models.DateTimeField("Дата редактирования", auto_now=True)

    imt = models.FloatField("ИМТ", blank=True, null=True)

    def save(self, *args, **kwargs):
        """Automatically calculate BMI from patient's data when possible."""
        if self.patient and self.patient.ves and self.patient.rost:
            try:
                self.imt = self.patient.ves / ((self.patient.rost / 100) ** 2)
            except ZeroDivisionError:
                self.imt = None
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Diagnosis #{self.pk}"

    class Meta:
        verbose_name_plural = "Формулы"
