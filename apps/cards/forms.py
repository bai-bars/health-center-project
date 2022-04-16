from django import forms

from .models import CardPerson, Guardian, FamilyMember

class CardPersonForm(forms.ModelForm):
    class Meta:
        model = CardPerson
        fields = '__all__'

class GuardianForm(forms.ModelForm):
    class Meta:
        model = Guardian
        fields = '__all__'

class FamilyMemberForm(forms.ModelForm):
    class Meta:
        model = FamilyMember
        fields= '__all__'