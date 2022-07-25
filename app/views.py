from PyPDF2 import PdfFileReader, PdfFileWriter, PdfFileMerger
from django.core.files import File
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from app.forms import MergeForm, SplitForm

from app.models import PDF


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
            PDF.objects.create(pdf=File(file=open('merged.pdf', 'rb'), name='merged_file.pdf'))

            messages.success(request, 'done successfully')

            return redirect(reverse_lazy('app:merge'))
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
                PDF.objects.create(pdf=File(file=open(f'{i}.pdf', 'rb'), name='merged_file.pdf'))

        messages.success(request, 'done successfully')
        return redirect(reverse_lazy('app:split'))

    else:
        split_form = SplitForm()

    context = {
        'upload_pdf_form': split_form
    }
    return render(request, 'app/split.html', context)
