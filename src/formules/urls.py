from . import views
from django.urls import path

urlpatterns = [
    path('', views.Index, name="Index"),
    path('api/formules/', views.formulesAPI, name="formulesAPI"),
    path('api/formules/add/', views.AddFormuleAPI, name="AddFormuleAPI"),
    path('api/formules/<int:id>/', views.formulesDetailsAPI, name="formulesDetailsAPI"),
    path('api/formules/edit/<int:id>/', views.EditFormuleAPI, name="EditFormuleAPI"),
    path('api/formules/delete/<int:id>/', views.DeleteFormuleAPI, name="DeleteFormuleAPI"),
    path('users/', views.users_view, name='users_view'),
    path('users/toggle_doctor/<int:user_id>/', views.toggle_doctor_role, name='toggle_doctor_role'),
    path('profile/', views.profile_edit, name='profile_edit'),
]
