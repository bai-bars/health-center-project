from .models import CardCategory


def card_categories(request):
    return {"card_categories": CardCategory.objects.all()}