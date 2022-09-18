from django.urls import path

from . import views

app_name = "patients"

urlpatterns = [
    path('entry/', views.AppointmentEntryView.as_view(), name= "appointment_entry"),
    path('history/', views.AppointmentHistoryView.as_view(), name= "appointment_history"),
    path('history-query/', views.AppointmentHistoryView.as_view(), name= "appointment_history_query"),
    path('history-update/', views.AppointmentUpdateView.as_view(), name= "appointment_update"),
    path('history-delete/', views.AppointmentDeleteView.as_view(), name= "appointment_delete"),
]
