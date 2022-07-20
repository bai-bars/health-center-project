from django.db import models

# Create your models here.
class AppOption(models.Model):
    key = models.CharField(max_length=50,primary_key=True,unique=True)
    value = models.IntegerField()

    class Meta:
        verbose_name_plural = 'App Options'

    def __str__(self):
        return f'({self.key}, {self.value})'