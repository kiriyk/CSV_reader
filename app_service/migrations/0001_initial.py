# Generated by Django 4.2.1 on 2023-06-04 22:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CSVFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='csv_files/', verbose_name='csv_files')),
                ('uploaded', models.DateField(auto_now=True, verbose_name='uploaded')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='file', to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
        ),
    ]
