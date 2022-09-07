from django.urls import path

from . import views

app_name = "patients"

urlpatterns = [
    path('entry/', views.AppointmentEntryView.as_view(), name= "appointment_entry" ),
]
