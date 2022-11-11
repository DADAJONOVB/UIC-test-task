from . import views
from django.urls import path, include

urlpatterns = [
    path('account/' ,include('rest_framework.urls')),
    path('create/application/', views.CreateSponsorAplicationView.as_view()),
    path('student/<int:pk>/', views.student_detail)
]