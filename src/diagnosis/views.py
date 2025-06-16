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
    return render(request, 'Index.html', context)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def diagnosisAPI(request):
    if request.user.groups.filter(name='Врач').exists():
        diagnosis = Diagnosis.objects.all().order_by('id')
    else:
        diagnosis = Diagnosis.objects.filter(patient=request.user).order_by('id')
    serializer = DiagnosisSerializer(diagnosis, many=True)
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
