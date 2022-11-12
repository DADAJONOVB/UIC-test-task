from . import serializers
from rest_framework import generics
from main import models
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.filters import  SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAdminUser


class CreateSponsorAplicationView(generics.CreateAPIView):
    queryset = models.SponsorAplication.objects.all()
    serializer_class = serializers.SponsorAplicationCreateSerializer


class SponsorDetailAplicationView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.SponsorAplication.objects.all()
    serializer_class = serializers.SponsorAplicationCreateSerializer
    permission_classes = (IsAdminUser, )

class SponsorAplicationListView(generics.ListAPIView):
    queryset = models.SponsorAplication.objects.all()
    serializer_class = serializers.SponsorAplicationCreateSerializer
    search_fields = ('full_name','organization',)
    filter_backends = [DjangoFilterBackend,]
    filterset_fields = ['aplication_type', 'payment_price', 'created']
    permission_classes = (IsAdminUser, )


class StudentListView(generics.ListAPIView):
    queryset = models.Student.objects.all()
    serializer_class = serializers.StudentSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('full_name','university',)
    filter_backends = [DjangoFilterBackend,]
    filterset_fields = ['university', 'type']
    permission_classes = (IsAdminUser, )



class StudentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Student.objects.all()
    serializer_class = serializers.StudentSerializer
    permission_classes = (IsAdminUser, )

    def get(self, request, pk):
        student = models.Student.objects.get(pk=pk)
        sponsor = models.Sponsor.objects.filter(student=student)
        student_serializer = serializers.StudentSerializer(student).data
        sponsor_serializer = serializers.SponserSerializer(sponsor, many=True).data
        data = {
            'student':student_serializer,
            'sponsor_serializer':sponsor_serializer
        }
        return Response(data, status=status.HTTP_200_OK)

class AddSponsorToStudent(generics.CreateAPIView):
    queryset = models.Sponsor.objects.all()
    serializer_class = serializers.SponserSerializerCreate
    permission_classes = (IsAdminUser, )


    def create(self, request):
        print(request.data)
        try:
            student_id = int(request.data.get('student'))
            sponsor_id = int(request.data.get('sponsor'))
            price = int(request.data.get('price'))
            student = models.Student.objects.get(id=student_id)
            sponsor = models.SponsorAplication.objects.get(id=sponsor_id)
            if sponsor.payment_price >=price:
                models.Sponsor.objects.create(
                    student=student,
                    sponsor=sponsor,
                    price=price
                ) 
                sponsor.payment_price-=price
                sponsor.spent_price += price
                data={
                    'suucess':True,
                    'status':status.HTTP_201_CREATED
                }
            else:
                price = price-sponsor.payment_price
                data = {
                    'success':False,
                    'data':'Homiyning pulida kamomat',
                    'kamomat':price,
                    'status':status.HTTP_400_BAD_REQUEST
                }
        except Exception as err:
            data = {
                'success':False,
                'error':f"{err}",
                'status':status.HTTP_400_BAD_REQUEST
            }
        return Response(data)



@api_view(['GET'])
@permission_classes([IsAdminUser])
def chart_data(request):
    label = ['YA', "FE", "MA", "AP", "MA", "IN", "IU", "AV", "SE", "OK", "NO", "DE"]
    sponsor = []
    student = []
    for i in range(1, 13):
        query1 = models.SponsorAplication.objects.filter(created__month=i).count()
        query2 = models.Student.objects.filter(created__month=i).count()
        sponsor.append(query1)
        student.append(query2)

    data = {
        "label":label,
        "sponsor":sponsor,
        "student":student
    }

    return Response(data)