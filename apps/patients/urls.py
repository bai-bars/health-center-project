from django.urls import path

from . import views

app_name = "patients"

urlpatterns = [
    path('entry/', views.appointment_entry_get, name= "appointment_entry" ),
]
