from django.shortcuts import render
from . import serializers
from rest_framework import generics
from main import models
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


class CreateSponsorAplicationView(generics.CreateAPIView):
    queryset = models.SponsorAplication.objects.all()
    serializer_class = serializers.SponsorAplicationCreateSerializer

class SponsorDetailAplicationView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.SponsorAplication.objects.all()
    serializer_class = serializers.SponsorAplicationCreateSerializer

class ponsorAplicationListView(generics.ListAPIView):
    queryset = models.SponsorAplication.objects.all()
    serializer_class = serializers.SponsorAplicationCreateSerializer

class StudentListView(generics.ListAPIView):
    queryset = models.Student.objects.all()
    serializer_class = serializers.StudentSerializer

class StudentDetailView(generics.UpdateAPIView):
    queryset = models.Student.objects.all()
    serializer_class = serializers.StudentSerializer

@api_view(['GET'])
def student_detail(request, pk):
    student = models.Student.objects.get(pk=pk)
    # serializer = serializers.StudentSerializer(stundent)
    # return Response(serializer.data, status=200)

    student = models.Student.objects.get(pk=pk)
    sponsor = models.Sponsor.objects.filter(student=student)
    student_serializer = serializers.StudentSerializer(student).data
    sponsor_serializer = serializers.SponserSerializer(sponsor, many=True).data
    # return Response(sponsor_serializer.data, status=200)
    data = {
        'student':student_serializer,
        'sponsor_serializer':sponsor_serializer
    }
    return Response(data, status=status.HTTP_200_OK)