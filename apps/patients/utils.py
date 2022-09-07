# from django.conf import settings
from pathlib import Path

import io
from datetime import timedelta
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from PyPDF2 import PdfFileReader, PdfFileWriter

BASE_DIR = Path(__file__).resolve().parent.parent.parent

class PrescriptionPDFGenerator:
    def __init__(self, patient_id):
        self.id = patient_id
        # self.output_filepath = settings.STATICFILES_DIRS[0] / 'files'  / 'prescription.pdf'
        self.output_filepath =  BASE_DIR / 'static' / 'files' / 'prescription.pdf'
        # self.template_filepath = settings.STATICFILES_DIRS[0] / 'files' / 'prescription_template.pdf'
        self.template_filepath = BASE_DIR / 'static' / 'files' / 'prescription_template.pdf'
        self.packet = io.BytesIO()
        self.mycanvas = canvas.Canvas(self.packet, pagesize=letter)

    def add_patient_id(self):
        self.mycanvas.setFont("Helvetica", 14)
        self.mycanvas.setFillColorRGB(0,0,1)
        self.mycanvas.drawString(75, 640, str(self.id))


    def add_serial_no(self, serial_no):
        self.mycanvas.setFont("Times-Bold", 15)
        self.mycanvas.setFillColorRGB(0,0,1)
        self.mycanvas.drawString(75, 610, str(serial_no))
    
    def add_date(self, date):
        date = date + timedelta(hours=6)

        self.mycanvas.setFont("Helvetica", 12)
        self.mycanvas.setFillColorRGB(0,0,1)

        self.mycanvas.drawString(485, 660, str(date.day))
        self.mycanvas.drawString(518, 660, str(date.month))
        self.mycanvas.drawString(548, 660, str(date.year))

    def add_name(self, name):
        self.mycanvas.setFont("Helvetica", 12)
        self.mycanvas.drawString(75, 580, name)
    
    def add_age(self, age):
        self.mycanvas.setFont("Helvetica", 12)
        self.mycanvas.drawString(75, 548, str(age))

    def add_gender(self, gender):
        self.mycanvas.setFont("Helvetica", 12)
        self.mycanvas.drawString(75, 518, str(gender))

    def add_card_id(self, card_id):
        self.mycanvas.setFont("Helvetica", 12)
        self.mycanvas.drawString(75, 488, str(card_id))

        
    
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


if __name__ == '__main__':
    pdf_obj = PrescriptionPDFGenerator(500014)
    pdf_obj.add_name("Nasif Anwar Khan Pallab")
    pdf_obj.add_age(21)
    pdf_obj.add_gender('Male')
    pdf_obj.add_card_id(10202202)
    pdf_obj.add_patient_id()
    pdf_obj.add_serial_no(14)

    import datetime

    pdf_obj.add_date(datetime.datetime.now())
    pdf_obj.create_pdf()
    print('Successful')