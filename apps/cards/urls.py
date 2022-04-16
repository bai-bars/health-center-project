from django.urls import path

from . import views

app_name = "cards"

urlpatterns = [
    path('card-person-entry/', views.card_person_entry, name= "card_person_entry" ),
    path('<str:card_id>/details/', views.card_person_details, name= "card_person_details" ),
    path('<str:card_id>/delete-card/', views.delete_card, name= "delete_card"),
    path('<str:card_id>/edit-card/', views.edit_card, name= "edit_card"),
    path('card-person-list/', views.card_person_list, name= "card_person_list"),
    path('search-card/', views.search_card, name= "search_card"),
]
