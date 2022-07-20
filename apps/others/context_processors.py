from .models import AppOption


def image_upload_option(request):
    return {"image_upload": AppOption.objects.get(pk='image_upload')}