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
    def __init__(self, *args, file_field_count, **kwargs):
        super().__init__(*args, **kwargs)

        for i in range(file_field_count):
            self.fields[f'file{i}'] = forms.FileField(label=f'PDF File {i + 1}')

    class Meta:
        model = Pdf  
        fields = [] 

    def clean(self):
        cleaned_data = super().clean()

        has_files = any(cleaned_data.get(f'file{i}') for i in range(len(self.fields)))
        if not has_files:
            raise forms.ValidationError("At least one file must be uploaded.")

        return cleaned_data
        
