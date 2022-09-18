# from django.db import models
# from django.utils import timezone
# # Create your models here.

# class DrugCategory(models.Model):
#     name = models.CharField(max_length=50, blank=False, null=True)
    
#     def __str__(self):
#         return str(self.name)
	

# class PharmaceuticalCompany(models.Model):
#     name = models.CharField(max_length=50, blank=True, null=True)
#     country = models.CharField(max_length=50, blank=True, null=True)


# class GenericDrug(models.Model):
#     name = models.CharField(max_length=55, blank=True, null=True)


# class DrugStock(models.Model):
#     name = models.CharField(max_length=50, blank=True, null=True)

#     category = models.ForeignKey(DrugCategory, null=True, blank=True, on_delete=models.CASCADE)
#     generic = models.ForeignKey(GenericDrug, blank=True, null=True)
#     company = models.ForeignKey(PharmaceuticalCompany, blank=True, null=True)

#     quantity = models.IntegerField(default='0', blank=True, null=True)
#     receive_quantity = models.IntegerField(default='0', blank=True, null=True)
#     reorder_level = models.IntegerField(default='0', blank=True, null=True)

#     last_updated = models.DateTimeField(auto_now_add=False, auto_now=True)
#     timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
#     drug_strength= models.CharField(max_length=10, blank=True, null=True)
#     valid_from = models.DateTimeField(blank=True, null=True,default=timezone.now)
#     valid_to = models.DateTimeField(blank=False, null=True)
#     drug_description=models.TextField(blank=True,max_length=1000,null=True)
#     drug_pic=models.ImageField(default="images2.png",null=True,blank=True)
   
#     def __str__(self):
#         return str(self.drug_name)
   
    
# class Dispense(models.Model):
    
#     patient_id = models.ForeignKey(Patients, on_delete=models.DO_NOTHING,null=True)
#     drug_id = models.ForeignKey(Stock, on_delete=models.SET_NULL,null=True,blank=False)
#     dispense_quantity = models.PositiveIntegerField(default='1', blank=False, null=True)
#     taken=models.CharField(max_length=300,null=True, blank=True)
#     stock_ref_no=models.CharField(max_length=300,null=True, blank=True)
#     instructions=models.TextField(max_length=300,null=True, blank=False)
#     dispense_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)

