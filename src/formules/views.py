from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import Group

def Index(request):
    return render(request, 'Index.html')

@api_view(['GET'])
def formulesAPI(request):
    if request.user.groups.filter(name='Doctor').exists():
        formules = Formules.objects.all().order_by('id')
    else:
        formules = Formules.objects.filter(patient=request.user).order_by('id')
    serializer = FormuleSerializer(formules, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def formulesDetailsAPI(request, id):
    obj = get_object_or_404(Formules, id=id)
    if request.user.groups.filter(name='Doctor').exists() or obj.patient == request.user:
        serializer = FormuleSerializer(obj, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_403_FORBIDDEN)


@api_view(['POST'])
def AddFormuleAPI(request):
    serializer = FormuleSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(patient=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def EditFormuleAPI(request, id):
    obj = get_object_or_404(Formules, id=id)
    if request.user.groups.filter(name='Doctor').exists() or obj.patient == request.user:
        serializer = FormuleSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save(patient=obj.patient)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_403_FORBIDDEN)

@api_view(['DELETE'])
def DeleteFormuleAPI(request, id):
    obj = get_object_or_404(Formules, id=id)
    if request.user.groups.filter(name='Doctor').exists() or obj.patient == request.user:
        obj.delete()
        return Response('Formule successfully Deleted!', status=status.HTTP_200_OK)
    return Response(status=status.HTTP_403_FORBIDDEN)
