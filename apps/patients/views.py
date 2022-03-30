from django.shortcuts import render

def patient_entry(request):
    return render(request, 'patients/patient_entry.html')
