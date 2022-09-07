from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.others.urls' , namespace = 'others')),
    path('patient/', include('apps.patients.urls' , namespace = 'patients')),
    path('doctor/', include('apps.doctors.urls' , namespace = 'doctor')),
    path('card/', include('apps.cards.urls' , namespace = 'cards')),
]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)