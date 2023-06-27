from django import forms  
from django.forms import ModelForm, widgets
from .models import Image, Pdf
from .widgets import MultiFileInput
from django import forms
from multiupload.fields import MultiFileField

class MyForm(forms.Form):
    files = MultiFileField(min_num=1, max_num=10, max_file_size=1024*1024*5)

class ImageForm(forms.ModelForm):
    """Form for the image model"""
    image = MultiFileField(min_num=1, max_num=10, max_file_size=1024*1024*5)
    class Meta:
        model = Image
        fields = ('image',)
        
class FileForm(forms.ModelForm):
    file1 = forms.FileField(label='PDF File 1')
    file2 = forms.FileField(label='PDF File 2')

    class Meta:
        model = Pdf
        fields = ('file1', 'file2')
        
