from PyPDF2 import PdfFileReader, PdfFileWriter, PdfFileMerger
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from app.forms import PDFForm
from django.contrib import messages


def merge(request):
    if request.method == 'POST':
        upload_pdf_form = PDFForm(request.POST, request.FILES)
        if upload_pdf_form.is_valid():
            pdf_files = request.FILES.getlist('pdf')
            out_file = PdfFileMerger()
            for pdf in pdf_files:
                out_file.append(pdf)
            with open('merged.pdf', 'wb') as output_stream:
                out_file.write(output_stream)
            messages.success(request, 'done successfully')
            return redirect(reverse_lazy('app:merge'))
    else:
        upload_pdf_form = PDFForm()

    context = {
        'upload_pdf_form': upload_pdf_form
    }
    return render(request, 'app/merge.html', context)
