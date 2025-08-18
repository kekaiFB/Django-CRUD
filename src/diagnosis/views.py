from django.shortcuts import render, redirect, get_object_or_404
from django import forms
from .models import *
from .serializers import *
from .forms import DiagnosisForm
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
# views.py
import random
from django.db import transaction
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Diagnosis
from .serializers import DiagnosisSerializer


@login_required
def Index(request):
    form = DiagnosisForm()
    if request.user.groups.filter(name='Врач').exists() or request.user.is_superuser:
        patient_group = Group.objects.filter(name='Пациент').first()
        if patient_group and 'patient' in form.fields:
            form.fields['patient'].queryset = patient_group.user_set.all().order_by('email')
    else:
        if 'patient' in form.fields:
            form.fields['patient'].widget = forms.HiddenInput()
    context = {
        'form': form,
    }
    context['is_doctor'] = request.user.groups.filter(name='Врач').exists()

    return render(request, 'Index.html', context)


@login_required
def PatientList(request):
    form = DiagnosisForm()
    if request.user.groups.filter(name='Врач').exists() or request.user.is_superuser:
        patient_group = Group.objects.filter(name='Пациент').first()
        if patient_group and 'patient' in form.fields:
            form.fields['patient'].queryset = patient_group.user_set.all().order_by('email')
    else:
        if 'patient' in form.fields:
            form.fields['patient'].widget = forms.HiddenInput()
    context = {
        'form': form,
    }
    context['is_doctor'] = request.user.groups.filter(name='Врач').exists()

    return render(request, 'patient.html', context)

# --- простые хелперы ---
def _maybe(val, p_none=0.15):
    """Вернуть значение или None с вероятностью p_none."""
    return None if random.random() < p_none else val

def _clamp(x, lo, hi):
    return max(lo, min(hi, x))

def _rint(lo, hi):
    return random.randint(lo, hi)

def _rfloat(lo, hi, nd=1):
    return round(random.uniform(lo, hi), nd)

User = get_user_model()


def _unique_username(ln: str, fn: str) -> str:
    base = f"{ln}-{fn}"
    cand, i = base, 1
    while User.objects.filter(username=cand).exists():
        i += 1
        cand = f"{base}-{i}"
    return cand

LAST_M = ["Иванов","Петров","Сидоров","Кузнецов","Смирнов","Попов","Фёдоров","Волков","Соловьёв","Егоров"]
LAST_F = ["Иванова","Петрова","Сидорова","Кузнецова","Смирнова","Попова","Фёдорова","Волкова","Соловьёва","Егорова"]
FIRST_M = ["Алексей","Иван","Сергей","Павел","Дмитрий","Антон","Никита","Артур","Владимир","Егор"]
FIRST_F = ["Мария","Ольга","Елена","Наталья","Анна","Татьяна","Ксения","Виктория","Юлия","Ирина"]
PATR_M  = ["Алексеевич","Иванович","Сергеевич","Павлович","Дмитриевич"]
PATR_F  = ["Алексеевна","Ивановна","Сергеевна","Павловна","Дмитриевна"]
DX = ["БА","ХОБЛ","Туберкулез","ТЭЛА","Пневмония","Бронхит"]

import string

def _random_email(ln: str, fn: str) -> str:
    # чуть перемешиваем, чтобы не дублировалось
    domain = random.choice(["gmail.com", "mail.ru", "yandex.ru", "outlook.com"])
    postfix = "".join(random.choices(string.digits, k=3))
    return f"{fn}.{ln}{postfix}@{domain}"




def _maybe(val, p_none=0.0):  # было 0.15
    return None if random.random() < p_none else val





def _vitals_by_dx(dx: str):
    """Немного правдоподобной корреляции под диагноз."""
    t = round(_clamp(random.gauss(36.8, 0.4), 35.5, 40.5), 1)
    sat = round(_clamp(random.gauss(97.5, 1.5), 88, 100), 1)
    chs = int(_clamp(random.gauss(78, 10), 50, 140))
    leu = round(_clamp(random.gauss(6.5, 2.0), 2.0, 30.0), 1)
    crp = round(_clamp(random.gauss(6.0, 8.0), 0.0, 300.0), 1)
    soe = round(_clamp(random.gauss(15.0, 10.0), 1.0, 100.0), 1)
    cons, och, pleur = 0, 0, 0


    if dx in ("Пневмония","Бронхит","БА","ХОБЛ","Туберкулез","ТЭЛА"):
        t   = round(_clamp(random.gauss(38.0, 0.6), 36.5, 40.5), 1)
        chs = int(_clamp(random.gauss(90, 12), 55, 150))
        leu  = round(_clamp(random.gauss(10.0, 4.0), 3.0, 28.0), 1)
        crp  = round(_clamp(random.gauss(30.0, 25.0), 0.0, 250.0), 1)
        soe  = round(_clamp(random.gauss(28.0, 12.0), 2.0, 90.0), 1)
        sat  = round(_clamp(random.gauss(95.0, 2.5), 85.0, 100.0), 1)
    if dx == "Пневмония":
        cons, och, pleur = 1, 1, random.randint(0,1)
    if dx in ("БА", "ХОБЛ"):
        sat = round(_clamp(random.gauss(94.0, 2.0), 85.0, 100.0), 1)
    return t, sat, chs, leu, crp, soe, cons, och, pleur

def _create_seed():
    with transaction.atomic():
        # for _ in range(10):
        #     gender = random.choices(["М","Ж"], weights=[0.48, 0.52])[0]
        #     if gender == "М":
        #         ln = random.choice(LAST_M); fn = random.choice(FIRST_M); pn = random.choice(PATR_M)
        #         height = round(_clamp(random.gauss(176, 7), 160, 200), 0)   # см
        #     else:
        #         ln = random.choice(LAST_F); fn = random.choice(FIRST_F); pn = random.choice(PATR_F)
        #         height = round(_clamp(random.gauss(164, 6), 150, 185), 0)   # см

        #     age = int(_clamp(round(random.gauss(45, 15)), 18, 85))
        #     # целевой ИМТ 19–32 с норм. шумом
        #     bmi = round(_clamp(random.gauss(26, 4), 17, 38), 1)
        #     weight = round(bmi * pow(height/100.0, 2), 1)

        #     username = _unique_username(ln, fn)
        #     user = User.objects.create(
        #         username=username,
        #         first_name=fn,
        #         last_name=ln,
        #         email=_random_email(ln, fn),
        #         pol=gender,
        #         vozrast=age,
        #         ves=weight,
        #         rost=height,
        #     )
        #     if hasattr(user, "set_unusable_password"):
        #         user.set_unusable_password()
        #         user.save(update_fields=["password"])

        #     dx = random.choice(DX)
        #     t, sat, chs, leu, crp, soe, cons, och, pleur = _vitals_by_dx(dx)


        #     # лёгочные: ОФВ1 и ЖЕЛ (л)
        #     ofv1 = round(_clamp(random.gauss(2.8 if gender=="Ж" else 3.2, 0.6), 0.8, 5.5), 2)
        #     zhel = round(_clamp(ofv1 + random.uniform(0.9, 2.5), 1.5, 7.5), 2)

        #     Diagnosis.objects.create(
        #         patient=user,
        #         diagnosis=dx,

        #         simptomy_dni=_maybe(random.randint(0, 21)),
        #         anamnez=_maybe(random.randint(0, 1)),
        #         kashel=_maybe(random.randint(0, 3)),
        #         mokrota=_maybe(random.randint(0, 1)),
        #         odyshka=_maybe(random.randint(0, 3)),
        #         temperatura=_maybe(t),
        #         pritplenie=_maybe(random.randint(0, 1)),
        #         oslablenie=_maybe(random.randint(0, 3)),
        #         vlazhnye_hripi=_maybe(random.randint(0, 1)),
        #         krepitaciya=_maybe(random.randint(0, 1)),
        #         suhie_hripi=_maybe(random.randint(0, 1)),
        #         distancnye_svistyashchie_hripi=_maybe(random.randint(0, 1)),
        #         saturaciya=_maybe(sat),
        #         chs=_maybe(chs),
        #         ofv1=_maybe(ofv1),
        #         zhel_ofv1=_maybe(zhel),
        #         limfadenopatiya=_maybe(random.randint(0, 1)),
        #         ochagi=_maybe(och),
        #         konsolidacii=_maybe(cons),
        #         fibrozno_kistoznye=_maybe(random.randint(0, 1)),
        #         polosti=_maybe(random.randint(0, 1)),
        #         fibroz=_maybe(random.randint(0, 1)),
        #         plevralnyj_vypot=_maybe(pleur),
        #         leykocity=_maybe(leu),
        #         palochko=_maybe(round(_clamp(random.gauss(5.0, 3.0), 0.0, 30.0), 1)),
        #         eozinofily=_maybe(round(_clamp(random.gauss(2.5, 1.5), 0.0, 15.0), 1)),
        #         soe=_maybe(soe),
        #         bak_srb=_maybe(crp),

        #         imt=_maybe(bmi),  # ИМТ считаем из роста/веса
        #     )

        #         # создаём ещё 10 с фиксированным диагнозом ХОБЛ
        
        for _ in range(10):
            gender = random.choices(["М","Ж"], weights=[0.48, 0.52])[0]
            if gender == "М":
                ln = random.choice(LAST_M); fn = random.choice(FIRST_M); pn = random.choice(PATR_M)
                height = round(_clamp(random.gauss(176, 7), 160, 200), 0)
            else:
                ln = random.choice(LAST_F); fn = random.choice(FIRST_F); pn = random.choice(PATR_F)
                height = round(_clamp(random.gauss(164, 6), 150, 185), 0)

            age = int(_clamp(round(random.gauss(50, 12)), 35, 85))
            bmi = round(_clamp(random.gauss(27, 3), 18, 38), 1)
            weight = round(bmi * pow(height/100.0, 2), 1)

            username = _unique_username(ln, fn)
            user = User.objects.create(
                username=username,
                first_name=fn,
                last_name=ln,
                email=_random_email(ln, fn),
                pol=gender,
                vozrast=age,
                ves=weight,
                rost=height,
            )
            if hasattr(user, "set_unusable_password"):
                user.set_unusable_password()
                user.save(update_fields=["password"])

            dx = "ХОБЛ"
            t, sat, chs, leu, crp, soe, cons, och, pleur = _vitals_by_dx(dx)

            ofv1 = round(_clamp(random.gauss(2.5 if gender=="Ж" else 3.0, 0.6), 0.7, 5.0), 2)
            zhel = round(_clamp(ofv1 + random.uniform(0.8, 2.2), 1.5, 7.0), 2)

            Diagnosis.objects.create(
                patient=user,
                diagnosis=dx,
                simptomy_dni=_maybe(random.randint(3, 21)),
                anamnez=_maybe(1),
                kashel=_maybe(random.randint(1, 3)),
                mokrota=_maybe(1),
                odyshka=_maybe(random.randint(1, 3)),
                temperatura=_maybe(t),
                pritplenie=_maybe(random.randint(0, 1)),
                oslablenie=_maybe(random.randint(1, 3)),
                vlazhnye_hripi=_maybe(random.randint(0, 1)),
                suhie_hripi=_maybe(1),
                distancnye_svistyashchie_hripi=_maybe(random.randint(0, 1)),
                saturaciya=_maybe(sat),
                chs=_maybe(chs),
                ofv1=_maybe(ofv1),
                zhel_ofv1=_maybe(zhel),
                leykocity=_maybe(leu),
                soe=_maybe(soe),
                bak_srb=_maybe(crp),
                imt=_maybe(bmi),
            )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def diagnosisAPI(request):
    # Сидим только если нет данных вовсе
    if Diagnosis.objects.count() < 3:
        _create_seed()  # та функция генерации, что выше, с CustomUser


    # Доступ: врач видит всё, пациент — только свои записи
    if request.user.groups.filter(name='Врач').exists():
        qs = Diagnosis.objects.all().order_by('id')
    else:
        qs = Diagnosis.objects.filter(patient=request.user).order_by('id')

    serializer = DiagnosisSerializer(qs, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def diagnosisDetailsAPI(request, id):
    obj = get_object_or_404(Diagnosis, id=id)
    if request.user.groups.filter(name='Врач').exists() or obj.patient == request.user:
        serializer = DiagnosisSerializer(obj, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_403_FORBIDDEN)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def AddDiagnosisAPI(request):
    data = request.data.copy()
    patient = request.user
    if request.user.groups.filter(name='Врач').exists() and data.get('patient'):
        User = get_user_model()
        try:
            patient = User.objects.get(id=data['patient'])
        except User.DoesNotExist:
            return Response({'patient': 'Invalid'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        data['patient'] = patient.id

    serializer = DiagnosisSerializer(data=data)
    if serializer.is_valid():
        serializer.save(patient=patient)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def EditDiagnosisAPI(request, id):
    obj = get_object_or_404(Diagnosis, id=id)
    if request.user.groups.filter(name='Врач').exists() or obj.patient == request.user:
        serializer = DiagnosisSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save(patient=obj.patient)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_403_FORBIDDEN)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def DeleteDiagnosisAPI(request, id):
    obj = get_object_or_404(Diagnosis, id=id)
    if request.user.groups.filter(name='Врач').exists() or obj.patient == request.user:
        obj.delete()
        return Response('Diagnosis successfully Deleted!', status=status.HTTP_200_OK)
    return Response(status=status.HTTP_403_FORBIDDEN)

@login_required
def users_view(request):
    user = request.user
    if not (user.is_superuser or user.groups.filter(name='Врач').exists()):
        return HttpResponseForbidden()
    User = get_user_model()
    users = User.objects.all().order_by('id').prefetch_related('groups')

    for u in users:
        u.is_doctor = u.groups.filter(name='Врач').exists()  # добавляем флаг

    context = {
        'users': users,
        'is_admin': user.is_superuser,
    }
    return render(request, 'users.html', context)

@login_required
def toggle_doctor_role(request, user_id):
    if not request.user.is_superuser:
        return HttpResponseForbidden()
    User = get_user_model()
    target = get_object_or_404(User, id=user_id)
    doctor_group, _ = Group.objects.get_or_create(name='Врач')
    if doctor_group in target.groups.all():
        target.groups.remove(doctor_group)
    else:
        target.groups.add(doctor_group)
    return redirect('users_view')


@login_required
def profile_edit(request):
    user = request.user
    if request.method == 'POST':
        user.pol = request.POST.get('pol') or None
        user.vozrast = request.POST.get('vozrast') or None
        user.ves = request.POST.get('ves') or None
        user.rost = request.POST.get('rost') or None
        user.save()
        return redirect('Index')
    return render(request, 'profile.html')
