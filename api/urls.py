from . import views
from django.urls import path, include

urlpatterns = [
    path('account/', include('rest_framework.urls')),
    path('sponsor/application/create/', views.CreateSponsorAplicationView.as_view()),
    path('sponsor/application/list/', views.SponsorAplicationListView.as_view()),
    path('sponsor/application/detail/<int:pk>/', views.SponsorDetailAplicationView.as_view()),
    path('student/list/', views.StudentListView.as_view()),
    path('student/<int:pk>/', views.StudentDetailView.as_view()),
    path('chart/', views.chart_data),
    path('sponsor/add/', views.AddSponsorToStudent.as_view()),
    path('get/user/', views.GetUserToken.as_view())
]