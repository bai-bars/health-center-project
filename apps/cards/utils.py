from django.conf import settings

import io
from datetime import timedelta
from barcode import Code128, writer
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from PyPDF2 import PdfFileReader, PdfFileWriter


class CardPDFGenerator:
    RELATIONSHIPS = {
        'FAT':'Father', 'MOT':'Mother',
        'HUS':'Husband', 'WIF':'Wife',
        'BRO':'Brother', 'SON':'Son',
        'DAU':'Daughter', 'UNC':'Uncle',
        'AUN':'Aunt'
    }

    def __init__(self,id):
        self.id = id
        self.output_filepath = settings.MEDIA_ROOT / 'static_cards' / f'{id}.pdf'
        self.template_filepath = settings.STATICFILES_DIRS[0] / 'files' / 'card_template.pdf'
        self.packet = io.BytesIO()
        self.mycanvas = canvas.Canvas(self.packet, pagesize=letter)

    def add_id(self):
        self.mycanvas.setFont("Helvetica", 6)
        self.mycanvas.setFillColorRGB(0,0,1)
        self.mycanvas.drawString(45,326.5, self.id)
    
    def add_name(self, name):
        self.mycanvas.setFont("Times-Bold", 7)
        self.mycanvas.drawString(80, 310, name)

    def add_profile_pic(self, img_path):
        self.mycanvas.drawImage(img_path, 25, 256.6, width=50, height=60)

    def add_barcode_pic(self, img_path):
        self.mycanvas.drawImage(img_path, 35, 210, width=100, height=30)

    def add_date(self, created, last_modified):

        created = created + timedelta(hours=6)
        last_modified = last_modified + timedelta(hours=6)
        # CREATED AND LAST MODIFIED lABEL
        self.mycanvas.setFont("Times-BoldItalic", 4)
        self.mycanvas.drawString(182, 368, 'Created:')
        self.mycanvas.drawString(182, 362, 'Last Modified:')
        
        # CREATED AND LAST MODIFIED DATE
        self.mycanvas.setFont("Times-Italic", 4)
        self.mycanvas.drawString(197, 368, f'{str(created.time())[:8]}, {created.date()}')
        self.mycanvas.drawString(207, 362, f'{str(last_modified.time())[:8]}, {last_modified.date()}')

        
    def add_family_member(self, memberList):
        self.mycanvas.setFont("Helvetica",5)
        left = 182
        bottom = 299
        for i, name in enumerate(memberList):
            self.mycanvas.drawString(left, bottom, f'{i+1}. {name}')
            bottom -= 8

    def add_rect(self):
        self.mycanvas.setStrokeColorRGB(.5, .5, .5)
        self.mycanvas.rect(25, 256.8, 50.3, 60, fill=0)

    def add_guardian(self, guardian_type=None, guardian_name=None):
        self.mycanvas.setFont("Times-Bold", 5)

        if guardian_type is not None and guardian_name is not None:
            self.mycanvas.drawString(80, 300, f'{guardian_type}:')

            self.mycanvas.setFont("Helvetica",5)
            self.mycanvas.drawString(103, 300, guardian_name)
        else:
            self.mycanvas.drawString(80, 300, 'Guardian:')


    def add_address(self, address=None):
        if address is not None:
            self.mycanvas.setFont("Times-Bold", 5)
            self.mycanvas.drawString(80, 284, 'Address:')

            self.mycanvas.setFont("Helvetica",4)
            address_lst = address.split(',')
            if len(address_lst)>1:
                self.mycanvas.drawString(100, 284, (',').join(address_lst[:2]))
                self.mycanvas.drawString(100, 278, (',').join(address_lst[2:]))
            else:
                self.mycanvas.drawString(102, 284, address)


    def add_contact_no(self, contact_no=None):
        if contact_no is not None:
            self.mycanvas.setFont("Times-Bold", 5)
            self.mycanvas.drawString(80, 292, 'Contact No:')

            self.mycanvas.setFont("Helvetica",5)        
            self.mycanvas.drawString(108, 292, contact_no)


    def create_pdf(self):
        self.mycanvas.save()
        self.packet.seek(0)
        new_pdf = PdfFileReader(self.packet)

        template_pdf = open(self.template_filepath, "rb")
        template_pdf_read =PdfFileReader(template_pdf)
        
        output_pdf_writer = PdfFileWriter()
        page = template_pdf_read.getPage(0)
        page.mergePage(new_pdf.getPage(0))
        output_pdf_writer.addPage(page)

        output_pdf = open( self.output_filepath, "wb")
        output_pdf_writer.write(output_pdf)

        template_pdf.close()
        output_pdf.close()

        return self.output_filepath


class BarcodeGenerator:
    def __init__(self, id):
        self.id = id
        self.filepath = settings.MEDIA_ROOT / 'static_barcodes' / id
        self.generate_barcode_img()
    
    def generate_barcode_img(self):
        barcode = Code128(self.id, writer.ImageWriter())
        options = {"module_height": 10, "text_distance": 2, "font_size": 0}
        self.filepath = barcode.save(self.filepath, options=options)
