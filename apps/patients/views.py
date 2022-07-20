from datetime import date

from django.shortcuts import redirect, render

from .models import Appointment, SerialTracker
from .forms import AppointmentForm
from .utils import generate_appointments_id


def appointment_entry_get(request):
    serial_obj = SerialTracker.objects.get(pk=1)
    serial_no = serial_obj.serial_no
    today_date = date.today()

    if serial_obj.cur_date == today_date:
        serial_no = serial_no + 1
    else:
        serial_no = 1


    return render(request, 'patients/appointment_entry.html', context = {'serial_no' : serial_no})


def appointment_entry_post(request):
    serial_obj = SerialTracker.objects.get(pk=1)
    serial_no = serial_obj.serial_no
    today_date = date.today()

    if serial_obj.cur_date == today_date:
        serial_no = serial_no + 1
    else:
        serial_no = 1
        serial_obj.cur_date = today_date

    # APPOINTMENT OBJECT ID
    appointment_id = generate_appointments_id(today_date, serial_no)
        
    # SERIAL OBJECT
    serial_obj.serial_no = serial_no
    serial_obj.save()

    # APPOINTMENT 
    appoint = AppointmentForm(request.POST)
    appoint.save(commit=False)

    appoint.id = appointment_id
    appoint.serial_no = serial_no
    appoint.save()

    redirect('/')