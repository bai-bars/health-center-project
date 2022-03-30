# from django.db import models

# class Patient(models.Model):
#     GENDER_CHOICES = [
#         ('F', 'Female'), 
#         ('M', 'Male') 
#     ]
#     name = models.CharField(max_length=100)
#     birth_date = models.DateField(blank = True, null = True)
#     gender = models.CharField(max_length=2, choices=GENDER_CHOICES, default= 'M')
#     blood_group = models.CharField(max_length=3, blank = True, null = True)
#     location = models.CharField(max_length=100, blank= True, null = True)
#     contact_no = models.CharField(max_length=15, blank=True, null = True)

# class Relationship(models.Model):
#     RELATIONSHIP_KIND_CHOICES = [
#         ('F', 'Father'), ('M', 'Mother'),
#         ('C', 'Children'), ('H', 'Husband'),
#         ('W', 'Wife'), ('S', 'Sibling'),
#     ]

#     kind = models.CharField(max_length=1, choices=RELATIONSHIP_KIND_CHOICES)

# class Family(models.Model):
#     patient = models.ForeignKey(Patient, on_delete= models.CASCADE)
#     relationship_kind = models.ForeignKey(Relationship, on_delete=models.CASCADE)
#     relative_name = models.CharField(max_length=100)

    
