import os

from django.conf import settings
from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.db.models import Q

from django.contrib import messages
from django.core import files
from django.core.files import File

from .models import CardPerson, Guardian, FamilyMember
from .forms import CardPersonForm, GuardianForm, FamilyMemberForm
from .utils import BarcodeGenerator, CardPDFGenerator

def card_person_entry(request):
    if request.method == 'POST':
        id = request.POST['card_id']
        members_lst = request.POST.getlist('members[]')
        card_person_form =  CardPersonForm(request.POST, request.FILES)

        try:
            for err in card_person_form.errors:
                    messages.error(request, f"Sorry, Something went wrong. Probably with {err}!")           

            if card_person_form.is_valid():
                card = card_person_form.save(commit=False)
               
                barcode_obj = BarcodeGenerator(id)
                barcode_file = open(barcode_obj.filepath , "rb")
                # SAVE TO CardPerson  TABLE
                card.barcode_photo.save(f"{id}.png", File(barcode_file))
                barcode_file.close()

                if len(request.POST['guardian-relationship']) > 0:
                    guardian_form = GuardianForm({
                        'card_holder' : id,
                        'relationship_with_guardian' : request.POST['guardian-relationship'],
                        'guardian_name' : request.POST['guardian-name']
                    })

                    if guardian_form.is_valid():
                        guardian_form.save()
                
                for name in members_lst:
                    family_member_form = FamilyMemberForm({
                                'card_holder' : id,
                                'name': name})

                    if family_member_form.is_valid:
                        family_member_form.save()
                
                card_person = CardPerson.objects.get(pk = id)

                # CREATE PDF
                cardpdf_obj = CardPDFGenerator(id)
                cardpdf_obj.add_name(card_person.name)
                cardpdf_obj.add_profile_pic(card_person.person_photo.path)
                cardpdf_obj.add_rect()
                cardpdf_obj.add_barcode_pic(card_person.barcode_photo.path)
                cardpdf_obj.add_address(card_person.address)

                if card_person.contact_no is not None:
                    cardpdf_obj.add_contact_no(card_person.contact_no)

                if len(request.POST['guardian-relationship']) > 0:
                    cardpdf_obj.add_guardian(guardian_name= request.POST['guardian-name'], 
                                        guardian_type= request.POST['guardian-relationship'])
                else:
                    cardpdf_obj.add_guardian()
            
                cardpdf_obj.add_date(card_person.created_at, card_person.last_modified_at)
                cardpdf_obj.add_family_member(members_lst)
                cardpdf_obj.add_id()
                cardpdf_obj.create_pdf()

                cardpdf_file = open(cardpdf_obj.output_filepath , "rb")
                card_person.card_pdf.save(f"{id}.pdf", File(cardpdf_file))
                cardpdf_file.close()

                return redirect('cards:card_person_details', card_id = id)
        except:
            messages.error(request, "Sorry, Something Went wrong. Try again!")

    return render(request, 'cards/card_person_entry.html')


def card_person_details(request, card_id):
    card_person = CardPerson.objects.get(pk = card_id)
    guardian = Guardian.objects.filter(card_holder = card_person).first()
    family_members = FamilyMember.objects.filter(card_holder = card_person)

    ctx = {'card_person' : card_person, 'guardian': guardian, 'family_members': family_members }
    return render(request, 'cards/card_details.html', context = ctx )


def card_person_list(request):
    card_person_list = CardPerson.objects.all().order_by('-created_at')
    return render(request, 'cards/card_person_list.html', context = {'card_person_list' : card_person_list})


def search_card(request):
    query = request.GET.get('q')
    searched_cards = CardPerson.objects.filter(card_id = query)
    return render(request, 'cards/search_card.html', context = {'searched_cards': searched_cards})

def search_card_json(request, query):
    searched_cards = CardPerson.objects.filter(Q(card_id__icontains = query) | Q(name__icontains = query)).values()
    return JsonResponse({'data': list(searched_cards)}, safe=False)


def delete_card(request, card_id):
    if request.method == 'POST':
        card_id = request.POST['card_id']
        try:
            CardPerson.objects.get(card_id = card_id).delete()
            messages.success(request, 'Successfully Deleted!')
            return redirect('cards:card_person_list')
        except:
            messages.error(request, 'Something Went Wrong!')

    return render(request, 'cards/delete_confirmation.html', {'card_id' : card_id})



# EDIT CARD PERSON TABLE INFO
def edit_card(request, card_id):   
    if request.method == 'POST':
        card_id = request.POST['card_id']

        card_person_instance = CardPerson.objects.get(card_id=card_id)
        card_person_form =  CardPersonForm(request.POST or None, request.FILES or None, instance = card_person_instance)
        
        if card_person_form.is_valid():
            card_person_form.save()

        guardian_instance = Guardian.objects.filter(card_holder = card_person_instance).first()


        guardian_form = GuardianForm({
                'card_holder' : card_id,
                'guardian_name': request.POST['guardian_name'],
                'relationship_with_guardian': request.POST['relationship_with_guardian']
                }, instance = guardian_instance)

        if guardian_form.is_valid():
            guardian_form.save()

        FamilyMember.objects.filter(card_holder = card_id).delete()

        members_lst = request.POST.getlist('members[]')
    
        for name in members_lst:
            family_member_form = FamilyMemberForm({
                        'card_holder' : card_id,
                        'name': name})

            if family_member_form.is_valid():
                family_member_form.save()

        # CREATE PDF
        cardpdf_obj = CardPDFGenerator(card_id)
        cardpdf_obj.add_name(card_person_instance.name)
        cardpdf_obj.add_profile_pic(card_person_instance.person_photo.path)
        cardpdf_obj.add_rect()
        cardpdf_obj.add_barcode_pic(card_person_instance.barcode_photo.path)
        cardpdf_obj.add_address(card_person_instance.address)

        if card_person_instance.contact_no is not None:
            cardpdf_obj.add_contact_no(card_person_instance.contact_no)

        if len(request.POST['relationship_with_guardian']) > 0:
            cardpdf_obj.add_guardian(guardian_name= request.POST['guardian_name'], 
                                    guardian_type= request.POST['relationship_with_guardian'])
        else:
            cardpdf_obj.add_guardian()
            
        cardpdf_obj.add_date(card_person_instance.created_at, card_person_instance.last_modified_at)
        cardpdf_obj.add_family_member(members_lst)
        cardpdf_obj.add_id()
        cardpdf_obj.create_pdf()


        os.remove(settings.MEDIA_ROOT / 'cards' / f'{card_id}.pdf')
        cardpdf_file = open(cardpdf_obj.output_filepath , "rb")
        card_person_instance.card_pdf.save(f"{card_id}.pdf", File(cardpdf_file))
        cardpdf_file.close()

        messages.success(request, 'Updated Succesfully!')

    return redirect('cards:card_person_details', card_id = card_id)


def card_person_stats(request):
    total_card = CardPerson.objects.count()
    total_male_card = CardPerson.objects.filter(gender='M').count()
    total_female_card = total_card - total_male_card

    cntx = {'total': total_card, 'male': total_male_card, 'female': total_female_card}

    return render(request, 'cards/card_person_stats.html', context=cntx)


def refresh_card(request):
    static_barcodes_dir = settings.MEDIA_ROOT / 'static_barcodes'
    static_barcodes_list = os.listdir(static_barcodes_dir)

    static_cards_dir = settings.MEDIA_ROOT / 'static_cards'
    static_cards_list = os.listdir(static_cards_dir)

    for file in static_barcodes_list:
        os.remove(static_barcodes_dir / file)

    for file in static_cards_list:
        os.remove(static_cards_dir / file)

    messages.success(request, 'Card System Refreshed Successfully!')
    return redirect('others:index')