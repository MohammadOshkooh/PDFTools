from PyPDF2 import PdfFileReader, PdfFileWriter, PdfFileMerger
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, FormView

from app.forms import PDFForm


def index(request):
    if request.method == 'POST':
        upload_pdf_form = PDFForm(request.POST, request.FILES)
        if upload_pdf_form.is_valid():
            pdf_files = request.FILES.getlist('pdf')
            out_file = PdfFileMerger()
            for pdf in pdf_files:
                out_file.append(pdf)
            with open('merged.pdf', 'wb') as output_stream:
                out_file.write(output_stream)



            # # split
            # input_pdf = PdfFileReader(pdf)
            # output_pdf = PdfFileWriter()
            # for i in range(10, 20):
            #     output_pdf.addPage(input_pdf.getPage(i))
            # with open('file.pdf', 'wb') as out:
            #     output_pdf.write(out)
    else:
        upload_pdf_form = PDFForm()

    context = {
        'upload_pdf_form': upload_pdf_form
    }
    return render(request, 'app/index.html', context)
