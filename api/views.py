from . import serializers
from rest_framework import generics
from main import models
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.filters import  SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

class CreateSponsorAplicationView(generics.CreateAPIView):
    """this class is used to write a sponsor application"""
    
    queryset = models.SponsorAplication.objects.all()
    serializer_class = serializers.SponsorAplicationCreateSerializer


class SponsorDetailAplicationView(generics.RetrieveUpdateDestroyAPIView):
    """Through this class, 
    you can get detailed information about the sponsor, 
    change its information and completely delete it"""

    queryset = models.SponsorAplication.objects.all()
    serializer_class = serializers.SponsorAplicationCreateSerializer
    permission_classes = (IsAdminUser, )

class SponsorAplicationListView(generics.ListAPIView):
    """This class is used to output a list of patrons. 
    With the paginator function, information is sent from 10 pages"""

    queryset = models.SponsorAplication.objects.all()
    serializer_class = serializers.SponsorAplicationCreateSerializer
    search_fields = ('full_name','organization',)
    filter_backends = [DjangoFilterBackend,]
    filterset_fields = ['aplication_type', 'payment_price', 'created']
    permission_classes = (IsAdminUser, )


class StudentListView(generics.ListAPIView):
    """This class is used to get the list of students, 
    it is sent in 10 parts through the pagination function, 
    there is a search system for the student according to the 
    name of the university and the year of study, 
    filtering is performed according to the university and student type"""

    queryset = models.Student.objects.all()
    serializer_class = serializers.StudentSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('full_name','university',)
    filter_backends = [DjangoFilterBackend,]
    filterset_fields = ['university', 'type']
    permission_classes = (IsAdminUser, )



class StudentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """This class is used to get detailed information about Studnet, 
    which you can delete and change."""

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
    """This is the class of adding a sponsor to a student. 
    Through this class you can add a sponsor to one student, 
    this class accepts the student, 
    sponsor and how much money the sponsor wants to transfer."""

    queryset = models.Sponsor.objects.all()
    serializer_class = serializers.SponserSerializerCreate
    permission_classes = (IsAdminUser, )

    def create(self, request):
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
    """this function returns data for the admin dashboard,"""

    label = ['YA', "FE", "MA", "AP", "MA", "IN", "IU", "AV", "SE", "OK", "NO", "DE"]
    sponsor = []
    student = []

    for i in range(1, 13):
        query1 = models.SponsorAplication.objects.filter(created__month=i).count()
        query2 = models.Student.objects.filter(created__month=i).count()
        sponsor.append(query1)
        student.append(query2)

    total_requested_price = 0
    for s in models.Student.objects.all():
        total_requested_price +=s.contract_price

    total_pay_price = 0
    for s in models.Sponsor.objects.all():
        total_pay_price += s.price
    price_to_be_payed = total_requested_price-total_pay_price
    if price_to_be_payed < 0:
        price_to_be_payed = 0
    data = {
        "label":label,
        "sponsor":sponsor,
        "student":student,
        "total_pay_price":total_pay_price,
        "total_requested_price":total_requested_price,
        "price_to_be_payed":price_to_be_payed
    }
    return Response(data)


class GetUserToken(APIView):
    serializer_class = serializers.GetUseTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        username = serializer.data['username']
        user = User.objects.get(username=username)
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username':user.username
        })