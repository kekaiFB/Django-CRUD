from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.http import HttpResponse

def Index(request):
    return render(request, 'Index.html')

@api_view(['GET'])
def formulesAPI(request):
    formules = Formules.objects.all().order_by('id')
    serializer = FormuleSerializer(formules, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def formulesDetailsAPI(request, id):
    obj = get_object_or_404(Formules, id=id)
    serializer = FormuleSerializer(obj, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def AddFormuleAPI(request):
    serializer = FormuleSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def EditFormuleAPI(request, id):
    obj = get_object_or_404(Formules, id=id)
    serializer = FormuleSerializer(obj, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_304_NOT_MODIFIED)

@api_view(['DELETE'])
def DeleteFormuleAPI(request, id):
    if request.is_ajax():
        obj = get_object_or_404(Formules, id=id)
        obj.delete()
        return Response('Formule successfully Deleted!', status=status.HTTP_200_OK)
    return Response("That Formule Doesn't Exists!", status=status.HTTP_204_NO_CONTENT)
