from django.db import models

# Create your models here.
class Doctor(models.Model):
    code_name = models.CharField(max_length=4)
    name = models.CharField(max_length= 60)
    medical_college = models.CharField(max_length= 100)
    mbbs_passing_year = models.DateField(null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    specialist_at = models.CharField(max_length= 100, null=True, blank=True)

    appointment_fee = models.IntegerField()


    
