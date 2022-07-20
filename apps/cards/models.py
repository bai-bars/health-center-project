from django.db import models
from django.urls import reverse

class CardCategory(models.Model):
    category = models.CharField(default='New discount', max_length= 25, primary_key=True, unique=True)
    doctor_fee_discount = models.IntegerField(default=0)
    test_fee_discount = models.IntegerField(default=0)
    medicine_fee_discount = models.IntegerField(default=0)
    

    class Meta:
        verbose_name_plural = "Card Categories"

    def __str__(self):
        return self.category


class CardPerson(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),('Female', 'Female')
        ]

    card_id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=150)
    age = models.IntegerField(blank=True, null=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    contact_no = models.CharField(max_length=15, blank=True, null=True)
    person_photo = models.ImageField(upload_to='persons/', default = "persons/default.png")
    barcode_photo = models.ImageField(upload_to='barcodes/',default = "default.jpg")
    card_pdf = models.FileField(upload_to = "cards/" , default = "default.jpg")
    category = models.ForeignKey(CardCategory, on_delete= models.PROTECT, related_name='persons')
    created_at = models.DateTimeField(auto_now_add = True)
    last_modified_at = models.DateTimeField(auto_now = True)

    class Meta:
        verbose_name_plural = "Card Persons"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("cards:card_person_details", kwargs={"card_id": self.pk})
    


class Guardian(models.Model):
    RELATIONSHIP_CHOICES = [
        ('Father','Father'), ('Mother','Mother'),
        ('Husband','Husband'), ('Wife','Wife'),
        ('Brother','Brother'), ('Sister', 'Sister'),
        ('Son', 'Son'), ('Daughter', 'Daughter'),
        ('Uncle', 'Uncle'), ('Aunt', 'Aunt')
    ]

    card_holder = models.OneToOneField(CardPerson, on_delete=models.CASCADE, related_name= 'guardian', primary_key=True)
    relationship_with_guardian = models.CharField(max_length=8, choices=RELATIONSHIP_CHOICES)
    guardian_name = models.CharField(max_length= 100)

    def __str__(self):
        return self.card_holder.name+" ---> "+self.guardian_name


class FamilyMember(models.Model):
    card_holder = models.ForeignKey(CardPerson, on_delete=models.CASCADE, related_name= 'members')
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Family Members"
    def __str__(self):
        return self.card_holder.name+" ---> "+self.name
