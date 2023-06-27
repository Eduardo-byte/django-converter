import PyPDF2
from django.shortcuts import render, redirect
#from time import gmtime, strftime
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
    """Process PDF files uploaded by users"""
    path = 'pdf_files/'

    if request.method == 'GET':
        # Delete existing files in the "pdf_files/" directory
        for pdf in os.listdir(path):
            os.remove(os.path.join(path, pdf))

    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)

        if form.is_valid():
            # Save all uploaded PDF files
            files = request.FILES.getlist('file')
            files_saved_names = []

            for file in files:
                file_form = form.save(commit=False)
                file_form.file = file
                file_form.save()

                # Get the current instance object to display in the template
                pdf_obj = form.instance
                pdf_path = pdf_obj.file.path
                pdf_name = basename(pdf_path)
                files_saved_names.append(pdf_name)

            merger = PyPDF2.PdfMerger()
            for pdf_file in os.listdir(path):
                pdf_path = os.path.join(path, pdf_file)
                merger.append(pdf_path)

            merged_pdf_path = os.path.join(path, 'merged.pdf')
            merger.write(merged_pdf_path)
            merger.close()

            # Provide the merged PDF file for download
            with open(merged_pdf_path, 'rb') as file:
                response = HttpResponse(file, content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="merged.pdf"'
                return response

    else:
        form = FileForm()

    return render(request, 'merge_pdf.html', {'form': form, 'uploaded': False})
