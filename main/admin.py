from django.contrib import admin
from . import models

admin.site.register(models.University)
admin.site.register(models.StudentType)
admin.site.register(models.Student)
admin.site.register(models.SponsorAplication)
admin.site.register(models.Sponsor)