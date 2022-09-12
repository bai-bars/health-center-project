import os
import datetime

from django.db import models
from django.core.files import File
from django.conf import settings

from .utils import PrescriptionPDFGenerator
from apps.cards.models import CardPerson
from apps.doctors.models import Doctor


class PrescriptionPDF(models.Model):
    pdf_file = models.FileField(upload_to = "prescriptions/" , default = "default.jpg")

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
    
    doctor_fee = models.PositiveIntegerField(default=0, null=True, blank=True)
    lab_fee = models.PositiveIntegerField(default=0, blank=True, null=True)

    is_doctor_fee_paid = models.BooleanField(default=False)
    is_lab_fee_paid = models.BooleanField(default=False)


    def calc_serial_no(self):
        serial_obj = SerialTracker.objects.get(pk=1)
        serial_no = serial_obj.serial_no
        today_date = datetime.date.today()

        if serial_obj.cur_date == today_date:
            serial_no = serial_no + 1
        else:
            serial_no = 1
            serial_obj.cur_date = today_date
    
    
        serial_obj.serial_no = serial_no
        serial_obj.save()

        return serial_no


    def add_pad(self, serial_no):
        serial = str(serial_no)
        ln = len(serial)
    
        if ln == 1:
            serial = '00' + serial
        elif ln == 2:
            serial= '0' + serial

        return serial


    def generate_appointments_id(self, serial_no):
        today_date = datetime.date.today()
        date = ('').join(str(today_date).split('-'))
    
        serial = self.add_pad(serial_no)

        return int(date+serial)

    def save(self, *args, **kwargs):
        
        if self.serial_no is None:
            self.serial_no = self.calc_serial_no()
            self.id = self.generate_appointments_id(self.serial_no)

            # CREATE PRESCRIPTION PDF
            pdf_obj = PrescriptionPDFGenerator(self.id)
            pdf_obj.add_name(self.patient_name if self.patient_name is not None or self.patient_name is not '' else '')
            pdf_obj.add_age(self.age if self.age is not None or self.age == '' else '')
            pdf_obj.add_gender('Male' if self.gender == 'M' else 'F')
            pdf_obj.add_card_id(self.card.card_id if self.card is not None else '')
            pdf_obj.add_patient_id()
            pdf_obj.add_serial_no(self.serial_no)
            pdf_obj.add_date(datetime.datetime.now())
            pdf_obj.create_pdf()

            pdf_file = open(pdf_obj.output_filepath , "rb")

            saved_pdf = PrescriptionPDF.objects.get(id=1)

            media_pres_dir = settings.MEDIA_ROOT / 'prescriptions'
            media_pres_list = os.listdir(media_pres_dir)

            for file in media_pres_list:
                os.remove(media_pres_dir / file)

            saved_pdf.pdf_file.save(f"prescription.pdf", File(pdf_file))
            pdf_file.close()
        
        super(Appointment, self).save(*args, **kwargs)



class SerialTracker(models.Model):
    cur_date = models.DateField()
    serial_no = models.IntegerField()

    def __str__(self):
        return f'date: {self.cur_date}, serial: {self.serial_no}'
