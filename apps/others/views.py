import os
from django.http import JsonResponse
from django.shortcuts import render
from django.conf import settings
from django.contrib import messages

from .models import AppOption

def index(request):
    static_barcodes_ln = len(os.listdir(settings.MEDIA_ROOT / 'static_barcodes'))
    static_cards_ln = len(os.listdir(settings.MEDIA_ROOT / 'static_cards'))
    ln = static_barcodes_ln + static_cards_ln
    
    return render(request, 'core/index.html', context= {'ln': ln})

def img_upload_check(request,flag):
    image_upload = AppOption.objects.get(pk = 'image_upload')
    data_dict = {}
    if flag == 'true':
        image_upload.value = 1
        data_dict['data'] = 'Turned On'
    elif flag == 'false':
        image_upload.value = 0
        data_dict['data'] = 'Turned Off!'
    
    image_upload.save()

    return JsonResponse(data_dict)
