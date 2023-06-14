from django.forms import widgets

class MultiFileInput(widgets.ClearableFileInput):
    def __init__(self, attrs=None):
        attrs = attrs or {}
        attrs['multiple'] = 'multiple'
        super().__init__(attrs)

    def value_from_datadict(self, data, files, name):
        upload_files = super().value_from_datadict(data, files, name)
        if upload_files and isinstance(upload_files, list):
            return [f for f in upload_files if f]
        return upload_files
