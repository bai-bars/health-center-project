from django.urls import path

from . import views

app_name = "patients"

urlpatterns = [
    path('entry/', views.AppointmentEntryView.as_view(), name= "appointment_entry"),
    path('history/', views.AppointmentHistoryView.as_view(), name= "appointment_history"),
    path('history-query/', views.AppointmentHistoryView.as_view(), name= "appointment_history_query"),
    path('history/<int:id>', views.AppointmentHistoryView.as_view(), name= "appointment_update_delete"),
]
