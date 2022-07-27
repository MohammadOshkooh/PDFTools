import os

from PyPDF2 import PdfFileReader, PdfFileWriter, PdfFileMerger
from django.core.files import File
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import TemplateView

from app.forms import MergeForm, SplitForm, PdfToWordForm

from app.models import PDF


class Index(TemplateView):
    template_name = 'app/index.html'


def merge(request):
    if request.method == 'POST':
        merge_form = MergeForm(request.POST, request.FILES)
        if merge_form.is_valid():
            # Pdf files uploaded by the user
            pdf_files = request.FILES.getlist('pdf')

            # Merging
            out_file = PdfFileMerger()
            for pdf in pdf_files:
                out_file.append(pdf)

            # Save merged file on local
            with open('merged.pdf', 'wb') as output_stream:
                out_file.write(output_stream)

            # Save merged file in the db
            pdf_model = PDF.objects.create(pdf=File(file=open('merged.pdf', 'rb'), name='file.pdf'))

            # Remove file in local after save in db
            os.remove('merged.pdf')

            messages.success(request, 'done successfully')

            return render(request, 'app/link.html', {'file': pdf_model, 'command': 'merge'})
    else:
        merge_form = MergeForm()

    context = {
        'upload_pdf_form': merge_form
    }
    return render(request, 'app/merge.html', context)


def split(request):
    if request.method == 'POST':
        split_form = SplitForm(request.POST, request.FILES)
        if split_form.is_valid():
            # Pdf file uploaded by the user
            pdf = split_form.cleaned_data.get('pdf')

            # Specified range by the user
            numbers_array = request.POST['array']  # [(x,y),(t,m)]  type:str

            # convert to x,y,t,m  type:str
            numbers_array = numbers_array.replace('[', '').replace(']', '').replace('(', '').replace(')', '')

            # convert to [x,y,t,m]  type:list
            numbers_array = numbers_array.split(',')

            # Splitting
            input_pdf = PdfFileReader(pdf)

            files = []

            # convert to (x,y) (t,m) and splitting
            for i in range(0, int(len(numbers_array) / 2)):
                output_pdf = PdfFileWriter()

                a = int(numbers_array[2 * i]) - 1
                b = int(numbers_array[2 * i + 1])

                for j in range(a, b):
                    output_pdf.addPage(input_pdf.getPage(j))

                # save file on the local
                with open(f'{i}.pdf', 'wb') as out:
                    output_pdf.write(out)

                # Save merged file in the db
                pdf_model = PDF.objects.create(pdf=File(file=open(f'{i}.pdf', 'rb'), name='file.pdf'))

                # Remove file in local after save in db
                os.remove(f'{i}.pdf')

                files.append(pdf_model)
        messages.success(request, 'done successfully')
        return render(request, 'app/link.html', {'files': files, 'command': 'split'})

    else:
        split_form = SplitForm()

    context = {
        'upload_pdf_form': split_form
    }
    return render(request, 'app/split.html', context)


def pdf_to_word(request):
    if request.method == 'POST':
        form = PdfToWordForm(request.POST, request.FILES)
        if form.is_valid():
            # get pdf
            pdf = form.cleaned_data.get('pdf')
            p = PdfFileMerger()
            p.append(pdf)

            # save file on the local
            with open('file.doc', 'wb') as out:
                p.write(out)

            # Save merged file in the db
            model = PDF.objects.create(pdf=File(file=open('file.doc', 'rb'), name='file.doc'))

            # Remove file in local after save in db
            os.remove('file.doc')

            messages.success(request, 'done successfully')

            return render(request, 'app/link.html', {'file': model, 'command': 'to_word'})

    else:
        form = PdfToWordForm()

    context = {
        'upload_pdf_form': form,
    }
    return render(request, 'app/pdf_to_word.html', context)
