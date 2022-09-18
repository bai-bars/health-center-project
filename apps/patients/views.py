from datetime import date

from django.conf import settings
from django.shortcuts import redirect, render
from django.contrib import messages
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



class AppointmentHistoryView(View):
    def get(self,request):
        query_set = Appointment.objects.all().order_by('-created_at')

        doctors = Doctor.objects.all()

        return render(request, 'patients/appointment_history.html',
                                context={'appointments' : query_set,
                                         'doctors' : doctors})


class AppointmentUpdateView(View):
    def post(self,request):
        patient_id = request.POST['patient_id']
        appoint = Appointment.objects.get(id = patient_id)

        appoint_form = AppointmentForm(request.POST, instance = appoint)

        if appoint_form.is_valid():
            appoint_form.save()

        return redirect('patients:appointment_history')


class AppointmentDeleteView(View):
    def post(self,request):
        try:
            Appointment.objects.get(id = request.POST['patient_id']).delete()
            messages.success(request, 'Successfully Deleted!')
        except:
            pass

        return redirect('patients:appointment_history')