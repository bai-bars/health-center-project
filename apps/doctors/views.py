from django.shortcuts import render
from django.views import generic

from apps.doctors.models import Doctor
# Create your views here.
def list_doctor_objects(request):
    doctor = Doctor.objects.all()

    return {'doctors' : doctor}