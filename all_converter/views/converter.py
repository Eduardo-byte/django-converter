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
from ..forms  import ImageForm



def converter_png(request):
    """Process images uploaded by users"""
    path = 'images/'
    
    if request.method == 'GET':
        # Delete existing images in the "media/images/" directory
        for image in os.listdir(path):   
            os.remove(os.path.join(path, image))

    pwd = os.getcwd()
    
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        
        if form.is_valid():
            # Save all uploaded images
            images = request.FILES.getlist('image')  # Replace 'image' with the name of the image field in your form
            saved_image_names = []
            
            for image in images:
                image_form = form.save(commit=False)
                image_form.image = image
                
                image_form.save()

                # Get the current instance object to display in the template
                img_obj = form.instance
                img_path = img_obj.image.path
                img_name = basename(img_path)
                img_name = os.path.splitext(img_name)[0]
                saved_image_names.append(f'{img_name}.png')

                # Convert the image to PNG and save it in the "media/images/" directory
                img_png = Image.open(img_path)
                img_png.save(os.path.join(path, f'{img_name}.png'), 'PNG')
            
            return render(request, 'converter_png.html', {'form': form, 'img_obj': img_obj, 'pwd': pwd, 'saved_image_names': saved_image_names, 'uploaded': True})
    else:
        form = ImageForm()
        
    return render(request, 'converter_png.html', {'form': form, 'pwd': pwd, 'uploaded': False})

def download_images(request):
    """Downloads the converted PNG images"""
    image_names = request.GET.getlist('image_names')  # Assumes the image names are passed as a query parameter in the URL
    zip_filename = 'converted_images.zip'

    with default_storage.open(zip_filename, 'wb') as zip_file:
        with zipfile.ZipFile(zip_file, 'w') as zf:
            for image_name in image_names:
                image_path = os.path.join('images/', image_name)
                zf.write(image_path, basename(image_path))
    
    response = HttpResponse(content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename={zip_filename}'
    
    with default_storage.open(zip_filename, 'rb') as zip_file:
        response.write(zip_file.read())
    
    default_storage.delete(zip_filename)
    
    return response
