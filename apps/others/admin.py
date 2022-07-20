from django.contrib import admin

from .models import AppOption

# Register your models here.
admin.site.register(AppOption)

admin.site.index_title = 'Admin Panel'
admin.site.site_header = "Singerkach Probashi Health Center"
admin.site.site_title= "Admin"
