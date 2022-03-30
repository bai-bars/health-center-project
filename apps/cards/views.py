from django.shortcuts import redirect, render
from django.core import files
from django.core.files import File

from .forms import CardPersonForm
from .models import CardPerson, Guardian
from .utils import BarcodeGenerator, CardPDFGenerator


def create_card(request):
    if request.method == 'POST':
        id = request.POST['card_id']
        card_person_form =  CardPersonForm(request.POST, request.FILES)
       
        if card_person_form.is_valid():
            print('INT THE VALID FORM')
            card = card_person_form.save(commit=False)

            barcode_obj = BarcodeGenerator(id)
            barcode_file = open(barcode_obj.filepath , "rb")
            card.barcode_photo.save(f"barcodes/{id}.png", File(barcode_file))
            barcode_file.close()

            saved_card = CardPerson.objects.get(pk = id)
            profile_url = saved_card.person_photo.url
            print(profile_url)
            
            barcode_url = saved_card.barcode_photo.url
            print(barcode_url)
            name = saved_card.name

            if len(request.POST['guardian-relationship']) > 0:
                guardian_relationship = request.POST['guardian-relationship']
                guardian_name = request.POST['guardian-name']

                guardian = Guardian.objects.create(card_holder = saved_card, 
                                    relationship_with_guardian = guardian_relationship,
                                    guardian_name = guardian_name)
                guardian.save()


            # cardpdf_obj = CardPDFGenerator(id)

            pdf_info = {
                'id': id, 'profile_url': profile_url, 'barcode_url': barcode_url,
                'name': name, 'memberList' : None,
            }
            # cardpdf_obj.create_pdf(id, profile_url, barcode_url,
            #                         saved_card.name, )

        return redirect('cards:add_family_members', card_id = id)

    return render(request, 'cards/create_card.html')


def add_family_members(request , card_id):
    return render(request, 'cards/add_family_members.html')