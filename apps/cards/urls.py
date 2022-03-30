from django.urls import path

from . import views

app_name = "cards"

urlpatterns = [
    path('create-card/', views.create_card, name= "create_card" ),
    path('<str:card_id>/add-family-members/', views.add_family_members, name= "add_family_members" ),
]
