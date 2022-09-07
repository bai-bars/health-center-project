from datetime import date

from django.conf import settings
from django.shortcuts import redirect, render
from django.views import View
from django.http import JsonResponse, HttpResponse

from .models import Appointment, SerialTracker, PrescriptionPDF
from .forms import AppointmentForm
from apps.doctors.models import Doctor
# from .utils import generate_appointments_id, get_serial_no


class AppointmentEntryView(View):
    def get(self, request):
        serial_obj = SerialTracker.objects.get(pk=1)
        serial_no = serial_obj.serial_no
        today_date = date.today()

        if serial_obj.cur_date == today_date:
            serial_no = serial_no + 1
        else:
            serial_no = 1


        doctors = Doctor.objects.all()
        return render(request, 'patients/appointment_entry.html', context = {'serial_no' : serial_no,
                                                                             'doctors' : doctors })


    def post(self, request):
        appoint = AppointmentForm(request.POST)
        
        if appoint.is_valid():
            appoint.save()

        
        saved_pdf =  PrescriptionPDF.objects.get(id=1)

        
        return redirect(saved_pdf.pdf_file.url)