# Generated by Django 4.2.2 on 2023-06-27 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('all_converter', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pdf',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='pdf_files/')),
            ],
        ),
    ]