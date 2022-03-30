from django.contrib import admin

from .models import CardCategory, CardPerson, Guardian, FamilyMember

class CardPesonAdmin(admin.ModelAdmin):
    readonly_fields = ('card_id',)

admin.site.register(CardCategory)
admin.site.register(CardPerson, CardPesonAdmin)
admin.site.register(Guardian)
admin.site.register(FamilyMember)