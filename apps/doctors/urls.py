from django.urls import path

from . import views

app_name = "doctors"

urlpatterns = [
    path('list-doctor-object/', views.list_doctor_objects, name= "list_doctor_obj" ),
]
