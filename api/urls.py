from . import views
from django.urls import path, include

urlpatterns = [
    path('account/' ,include('rest_framework.urls')),
    path('sponsor/application/create/', views.CreateSponsorAplicationView.as_view()),
    path('sponsor/application/list/', views.SponsorAplicationListView.as_view()),
    path('sponsor/application/detail/<int:pk>/', views.SponsorDetailAplicationView.as_view()),
    path('student/list/', views.StudentListView.as_view()),
    path('student/<int:pk>/', views.StudentDetailView.as_view()),
    path('add/student/sponsor/', views.add_sponsor_to_student),
    path('chart/', views.chart_data)
]