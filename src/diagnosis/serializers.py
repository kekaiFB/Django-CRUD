from .models import *
from rest_framework import serializers


class DiagnosisSerializer(serializers.ModelSerializer):
    fio = serializers.CharField(source='patient.email', read_only=True)
    pol = serializers.CharField(source='patient.pol', read_only=True)
    vozrast = serializers.IntegerField(source='patient.vozrast', read_only=True)
    ves = serializers.FloatField(source='patient.ves', read_only=True)
    rost = serializers.FloatField(source='patient.rost', read_only=True)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        placeholders = {
            'simptomy_dni': "(до 5 дней., 5-10, более 10, более 15)",
            'anamnez': "ССЗ – да (0), нет (1), Сердечная недостаточность, СД",
            'kashel': "Непродуктивный (7-10), Влажный (4-6), Покашливание (0-3)",
            'mokrota': "1 - слизистая, 2 - слиз-гнойная, 3 - гнойная",
            'odyshka': "0 — нет, 10 — сильная отдышка",
            'temperatura': "Субфебрильная 37-37.9, Фебрильная 38-40",
            'pritplenie': "1 — есть, 0 — нет",
            'oslablenie': "1 — есть, 0 — нет",
            'auskultaciya': "1 — влажн. хрипы, 2 — крепитация, 3 — сухие хрипы, 4 — свист",
            'limfadenopatiya': "1 — есть, 0 — нет",
            'ochagi': "1 — есть, 0 — нет",
            'konsolidacii': "1 — есть, 0 — нет",
            'fibrozno_kistoznye': "1 — есть, 0 — нет",
            'polosti': "1 — есть, 0 — нет",
            'fibroz': "1 — есть, 0 — нет",
            'plevralnyj_vypot': "1 — есть, 0 — нет",
        }

        for field_name, placeholder in placeholders.items():
            if field_name in self.fields:
                self.fields[field_name].style = {'placeholder': placeholder}

    class Meta:
        model = Diagnosis
        fields = '__all__'