from django.db import models
from barcode import Code128

class CardCategory(models.Model):
    CATEGORY_CHOICES = [
        ('P', 'POOR'), ('NP', 'NOT POOR'),('NC', 'NO CARD')
    ] 
    category = models.CharField(max_length=2, choices= CATEGORY_CHOICES, primary_key=True, unique=True)

    class Meta:
        verbose_name_plural = "Card Categories"

    def __str__(self):
        return self.category


class CardPerson(models.Model):
    GENDER_CHOICES = [
        ('M', 'MALE'),('F', 'FEMALE')
        ]

    card_id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=150, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M')
    contact_no = models.CharField(max_length=15, blank=True, null=True)
    person_photo = models.ImageField(upload_to='persons/', default = "default.jpg")
    barcode_photo = models.ImageField(default = "default.jpg")
    card_pdf = models.FileField(upload_to = "cards/" , default = "default.jpg")
    category = models.ForeignKey(CardCategory, on_delete= models.PROTECT, blank= True, null = True, related_name='persons')

    class Meta:
        verbose_name_plural = "Card Persons"

    def __str__(self):
        return self.name


class Guardian(models.Model):
    RELATIONSHIP_CHOICES = [
        ('FAT', 'FATHER'),('MOT', 'MOTHER'),
        ('HUS', 'HUSBAND'),('WIF', 'WIFE'),
        ('BRO', 'BROTHER'),('SON', 'SON'),
        ('DAU', 'DAUGHTER'),('UNC', 'UNCLE'),
        ('AUN', 'AUNT'),
    ]
    card_holder = models.OneToOneField(CardPerson, on_delete=models.CASCADE, related_name= 'guardian', primary_key=True)
    relationship_with_guardian = models.CharField(max_length=3, choices=RELATIONSHIP_CHOICES)
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
