import os

from django.shortcuts import render
from django.conf import settings
from django.contrib import messages

def index(request):
    static_barcodes_ln = len(os.listdir(settings.MEDIA_ROOT / 'static_barcodes'))
    static_cards_ln = len(os.listdir(settings.MEDIA_ROOT / 'static_cards'))

    ln = static_barcodes_ln + static_cards_ln

    messages.info(request,f'{ln} Unnecessary Garbage File Deteted!')
    
    return render(request, 'core/index.html',)
