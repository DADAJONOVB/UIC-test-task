from main import models
from rest_framework import serializers



class SponsorAplicationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SponsorAplication
        exclude = ('aplication_type',)


class SponsorAplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SponsorAplication
        fields = '__all__'


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Student
        fields = '__all__'


class SponserSerializer(serializers.ModelSerializer):
    student = StudentSerializer(many=True, read_only=True)
    sponsor = SponsorAplicationSerializer(many=True, read_only=True)
    class Meta:
        model = models.Sponsor
        fields = ['id', 'sponsor', 'student', 'price']


class SponserSerializerCreate(serializers.ModelSerializer):
     class Meta:
        model = models.Sponsor
        fields = '__all__'


class GetUseTokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)