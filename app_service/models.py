from django.contrib.auth.models import User
from django.db import models


class CSVFile(models.Model):
    """
    Модель csv файла
    """
    file = models.FileField(upload_to='csv_files/', verbose_name='csv_files')
    uploaded = models.DateField(auto_now=True, verbose_name='uploaded')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='file', verbose_name='user')
