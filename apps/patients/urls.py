from django.urls import path

from . import views

app_name = "patients"

urlpatterns = [
    path('entry/', views.patient_entry, name= "patient_entry" )
]
