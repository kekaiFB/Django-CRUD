from django import forms
from .models import Diagnosis


class DiagnosisForm(forms.ModelForm):
    class Meta:
        model = Diagnosis
        fields = '__all__'
        widgets = {
            'saturaciya': forms.NumberInput(attrs={'step': 'any'}),
            'ofv1': forms.NumberInput(attrs={'step': 'any'}),
            'zhel_ofv1': forms.NumberInput(attrs={'step': 'any'}),
            'leykocity': forms.NumberInput(attrs={'step': 'any'}),
            'palochko': forms.NumberInput(attrs={'step': 'any'}),
            'eozinofily': forms.NumberInput(attrs={'step': 'any'}),
            'soe': forms.NumberInput(attrs={'step': 'any'}),
            'bak_srb': forms.NumberInput(attrs={'step': 'any'}),
            'imt': forms.NumberInput(attrs={'step': 'any'}),
        }

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
                self.fields[field_name].widget.attrs.setdefault('placeholder', placeholder)
        if 'imt' in self.fields:
            self.fields['imt'].disabled = True

            
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
