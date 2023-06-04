from django.forms import ModelForm

from .models import CSVFile


class FileUploadForm(ModelForm):
    class Meta:
        model = CSVFile
        fields = ['file']
