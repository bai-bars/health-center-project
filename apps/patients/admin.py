from django.contrib import admin

from .models import Appointment, SerialTracker, PrescriptionPDF

# Register your models here.
class AppointmentAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'serial_no','created_at', 'updated_at')

admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(SerialTracker)
admin.site.register(PrescriptionPDF)