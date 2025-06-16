from . import views
from django.urls import path

urlpatterns = [
    path('', views.Index, name="Index"),
    path('api/diagnosis/', views.diagnosisAPI, name="diagnosisAPI"),
    path('api/diagnosis/add/', views.AddFormuleAPI, name="AddFormuleAPI"),
    path('api/diagnosis/<int:id>/', views.diagnosisDetailsAPI, name="diagnosisDetailsAPI"),
    path('api/diagnosis/edit/<int:id>/', views.EditFormuleAPI, name="EditFormuleAPI"),
    path('api/diagnosis/delete/<int:id>/', views.DeleteFormuleAPI, name="DeleteFormuleAPI"),
    path('users/', views.users_view, name='users_view'),
    path('users/toggle_doctor/<int:user_id>/', views.toggle_doctor_role, name='toggle_doctor_role'),
    path('profile/', views.profile_edit, name='profile_edit'),
]
