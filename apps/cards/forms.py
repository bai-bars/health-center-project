from pyexpat import model
from django import forms

from .models import CardPerson

class CardPersonForm(forms.ModelForm):
    class Meta:
        model = CardPerson
        fields = '__all__'
