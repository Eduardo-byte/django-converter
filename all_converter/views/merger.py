import PyPDF2
from django.shortcuts import render, redirect
from ..models import Image
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.http import FileResponse
from django.conf import settings
import io
from PIL import Image, ImageFilter
import sys
import os
from os.path import basename
import errno
import pathlib
from django.core.files.storage import default_storage
import zipfile
from ..forms  import FileForm


def merge_pdf(request):
    path = 'pdf_files/'
    fileFieldCount = 2  

    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES, file_field_count=fileFieldCount)

        if form.is_valid():
            pdf_instances = []

            for i in range(fileFieldCount):
                file_field_name = f'file{i}'
                if file_field_name in request.FILES:
                    pdf_instance = form.save(commit=False)
                    pdf_instance.file = request.FILES[file_field_name]
                    pdf_instance.save()
                    pdf_instances.append(pdf_instance)

            merger = PyPDF2.PdfMerger()
            for pdf_file in os.listdir(path):
                pdf_path = os.path.join(path, pdf_file)
                merger.append(pdf_path)

            merged_pdf_path = os.path.join(path, 'merged.pdf')
            merger.write(merged_pdf_path)
            merger.close()

            with open(merged_pdf_path, 'rb') as file:
                response = HttpResponse(file.read(), content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="merged.pdf"'
                return response

    else:
        form = FileForm(file_field_count=fileFieldCount)

    return render(request, 'merge_pdf.html', {'form': form, 'uploaded': False})
