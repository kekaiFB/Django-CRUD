from . import views
from django.urls import path

urlpatterns = [
    path('', views.Index, name="Index"),
    path('api/formules/', views.formulesAPI, name="formulesAPI"),
    path('api/formules/add/', views.AddFormuleAPI, name="AddFormuleAPI"),
    path('api/formules/<int:id>/', views.formulesDetailsAPI, name="formulesDetailsAPI"),
    path('api/formules/edit/<int:id>/', views.EditFormuleAPI, name="EditFormuleAPI"),
    path('api/formules/delete/<int:id>/', views.DeleteFormuleAPI, name="DeleteFormuleAPI"),
]
