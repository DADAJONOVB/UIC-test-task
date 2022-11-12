from django.db import models


class University(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class StudentType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Student(models.Model):
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    created = models.DateField(auto_now_add=True)
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    type = models.ForeignKey(
        StudentType, 
        on_delete=models.SET_NULL, 
        null=True
    )
    contract_price = models.IntegerField()

    def __str__(self):
        return self.full_name


class SponsorAplication(models.Model):
    TYPE = (
        (1, 'Jisminoiy Shaxs'),
        (2, 'Yuridik shaxs'),
    )
    APPLICATION_TYPE = (
        (1, 'Yangi'),
        (2, 'Modernizatsiya'),
        (3, 'Tasdiqlangan'),
        (4, 'Bekor qilingan'),
    )
    PAYMENT_TYPE = (
        (1, 'Naqt'),
        (2, 'Karta'),
        (3, 'Pul o`tkazma'),
    )
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    payment_price = models.IntegerField()
    spent_price = models.IntegerField(blank=True, null=True, default=0)
    created = models.DateField(auto_now_add=True)
    type = models.SmallIntegerField(choices=TYPE, default=1)
    aplication_type = models.SmallIntegerField(choices=APPLICATION_TYPE, default=1)
    payment_type = models.SmallIntegerField(choices=PAYMENT_TYPE)
    organization = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.full_name


class Sponsor(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    sponsor = models.ForeignKey(SponsorAplication, on_delete=models.CASCADE)
    price = models.IntegerField()

    def __str__(self):
        return str(self.sponsor.full_name)