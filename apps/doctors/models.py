from django.db import models

# Create your models here.
class Doctor(models.Model):
    code_name = models.CharField(max_length=4, blank=True,null=True)
    name = models.CharField(max_length= 60, blank=True,null=True)
    medical_college = models.CharField(max_length= 100, blank=True,null=True)
    mbbs_passing_year = models.DateField(null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    specialist_at = models.CharField(max_length= 100, null=True, blank=True)

    appointment_fee = models.IntegerField( blank=True,null=True)

    def __str__(self):
        return f'{self.name} ({self.code_name})'



    
