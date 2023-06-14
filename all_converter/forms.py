from django import forms  
from django.forms import ModelForm, widgets
from .models import Image
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