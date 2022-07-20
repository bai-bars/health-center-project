from django.urls import path

from . import views
app_name = "others"

urlpatterns = [
    path('', views.index, name='index'),
    path('img-upload-check/<str:flag>', views.img_upload_check, name='img_upload_check'),
]
