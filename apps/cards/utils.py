from django.conf import settings
from barcode import Code128, writer
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.pagesizes import letter
from PyPDF2 import PdfFileReader, PdfFileWriter
import io

class CardPDFGenerator:
    def __init__(self,id):
        self.output_filepath = settings.MEDIA_ROOT / 'static_cards' / id
        self.template_filepath = settings.STATICFILES_DIRS[0] / 'files' / 'card_template.pdf'
        self.packet = io.BytesIO()
        self.mycanvas = canvas.Canvas(self.packet, pagesize=letter)

    def add_id(self, can, id):
        self.mycanvas.setFont("Helvetica", 6)
        self.mycanvas.setFillColorRGB(0,0,1)
        self.mycanvas.drawString(45,326.5, id)
    
    def add_name(self, can, name):
        self.mycanvas.setFont("Times-Bold", 7)
        self.mycanvas.drawString(80, 310, name)

    def add_profile_pic(self, img_url):
        img = ImageReader(img_url)
        self.mycanvas.drawImage(img, 25, 256.6, width=100, height=60)

    def add_barcode_pic(self, img_url):
        img = ImageReader(img_url)
        self.mycanvas.drawImage(img, 35, 210, width=100, height=30)
        
    def add_family_member(self, memberList):
        left = 182
        bottom = 299
        for i, name in enumerate(memberList):
            self.mycanvas.drawString(left, bottom, f'{i}. {name}')
            bottom -= 8

    def add_rect(self):
        self.mycanvas.setStrokeColorRGB(.5, .5, .5)
        self.mycanvas.rect(25, 256.8, 50.3, 60, fill=0)

    def other_info(self, guardian_type=None, guardian_name=None, location=None, contact_no=None):
        self.mycanvas.setFont("Helvetica",5)
        # Guardian NAME
        if guardian_name is not None:
            self.mycanvas.drawString(98, 300, guardian_name) 
        # lOCATION
        if location is not None:
            location_lst = location.split(',')
            if len(location_lst>1):
                self.mycanvas.drawString(102, 284, (',').join(location_lst[:2]))
                self.mycanvas.drawString(102, 278, (',').join(location_lst[2:]))
            else:
                self.mycanvas.drawString(102, 284, location)

        # CONTACT NUMBER
        if contact_no is not None:
            self.mycanvas.drawString(108, 292, contact_no)
        
        # BOLD FONT
        self.mycanvas.setFont("Times-Bold", 5)
        self.mycanvas.drawString(80, 300, guardian_type)
        self.mycanvas.drawString(80, 292, 'Contact No:')
        self.mycanvas.drawString(80, 284, 'Address:')

    
    def create_pdf(self, kwargs):
        self.add_id(kwargs['id'])
        self.add_profile_pic(kwargs['profile_url'])
        self.add_barcode_pic(kwargs['barcode_url'])
        self.add_name(kwargs['name'])
        self.other_info(guardian_type = kwargs['guardian_type'], guardian_name= kwargs['guardian_name'], location = kwargs['location'])
        self.add_family_member(kwargs['memberList'])

        self.add_rect()

        self.mycanvas.save()
        self.packet.seek(0)
        new_pdf = PdfFileReader(self.packet)

        template_pdf = open(self.template_filepath, "rb")
        template_pdf_read =PdfFileReader(template_pdf)
        
        output_pdf_writer = PdfFileWriter()
        page = template_pdf_read.getPage(0)
        page.mergePage(new_pdf.getPage(0))
        output_pdf_writer.addPage(page)

        output_pdf = open(f'{self.output_filepath}.pdf', "wb")
        output_pdf_writer.write(output_pdf)

        template_pdf.close()
        output_pdf.close()

        return f'{self.output_filepath}.pdf'


class BarcodeGenerator:
    def __init__(self, id):
        self.id = id
        self.filepath = settings.MEDIA_ROOT / 'static_barcodes' / id
        self.generate_barcode_img()
    
    def generate_barcode_img(self):
        barcode = Code128(self.id, writer.ImageWriter())
        options = {"module_height": 10, "text_distance": 2, "font_size": 0}
        self.filepath = barcode.save(self.filepath, options=options)
