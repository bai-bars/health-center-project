from datetime import date

from django.db import models
from django.conf import settings

from .utils import generate_appointments_id
from apps.cards.models import CardPerson
from apps.doctors.models import Doctor

class Appointment(models.Model):
    GENDER_CHOICES = [
        ('F', 'Female'), 
        ('M', 'Male') 
    ]
    id = models.BigIntegerField(primary_key=True)
    serial_no = models.IntegerField()
    card = models.ForeignKey(CardPerson, null=True, blank=True,
                            related_name='patients', on_delete= models.SET_NULL)
    doctor = models.ForeignKey(Doctor, null=True, blank=True, related_name='appointments',
                               on_delete= models.SET_NULL)
    patient_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=2, choices=GENDER_CHOICES, default= 'M')
    age = models.PositiveIntegerField(null=True, blank=True)
    blood_group = models.CharField(max_length=3, blank = True, null = True)
    location = models.CharField(max_length=100, blank= True, null = True)
    contact_no = models.CharField(max_length=15, blank=True, null = True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    doctor_fee = models.PositiveIntegerField(default=0)
    lab_fee = models.PositiveIntegerField(default=0)

    is_doctor_fee_paid = models.BooleanField(default=False)
    is_lab_fee_paid = models.BooleanField(default=False)

    
    # def save(self, *args, **kwargs):
    #     serial_obj = SerialTracker.objects.get(pk=1)
    #     serial_no = serial_obj.serial_no
    #     today_date = date.today()

    #     if serial_obj.cur_date == today_date:
    #         serial_no = serial_no + 1
    #     else:
    #         serial_no = 1
    #         serial_obj.cur_date = today_date

    #     # APPOINTMENT OBJECT ID
    #     id = generate_appointments_id(today_date, serial_no)
        
    #     if not Appointment.objects.filter(pk = id).exists():
    #         # SERIAL OBJECT
    #         serial_obj.serial_no = serial_no
    #         serial_obj.save()

    #         # APPOINTMENT OBJECT
    #         self.id = id
    #         self.serial_no = serial_no

    #     super(Appointment, self).save(*args, **kwargs)



class SerialTracker(models.Model):
    cur_date = models.DateField()
    serial_no = models.IntegerField()

    def __str__(self):
        return f'date: {self.cur_date}, serial: {self.serial_no}'