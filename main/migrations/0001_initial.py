# Generated by Django 4.1.3 on 2022-11-11 18:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SponsorAplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=255)),
                ('payment_price', models.IntegerField()),
                ('created', models.DateField(auto_now_add=True)),
                ('type', models.SmallIntegerField(choices=[(1, 'Jisminoiy Shaxs'), (2, 'Yuridik shaxs')], default=1)),
                ('aplication_type', models.SmallIntegerField(choices=[(1, 'Yangi'), (2, 'Modernizatsiya'), (3, 'Tasdiqlangan'), (4, 'Bekor qilingan')], default=1)),
                ('payment_type', models.SmallIntegerField(choices=[(1, 'Naqt'), (2, 'Karta'), (3, 'Pul o`tkazma')])),
                ('organization', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='StudentType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='University',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=255)),
                ('contract_price', models.IntegerField()),
                ('type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.studenttype')),
                ('university', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.university')),
            ],
        ),
        migrations.CreateModel(
            name='Sponsor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.IntegerField()),
                ('sponsor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.sponsoraplication')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.student')),
            ],
        ),
    ]