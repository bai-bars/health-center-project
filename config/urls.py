from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('patient/', include('apps.patients.urls' , namespace = 'patients')),
    path('card/', include('apps.cards.urls' , namespace = 'cards')),
]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)