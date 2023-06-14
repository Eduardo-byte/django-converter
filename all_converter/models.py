from django.db import models
from django.contrib.auth.models import User
import datetime
from django import forms

# Create your models here.

class Image(models.Model):
    image = models.ImageField(upload_to='images/')
    title = models.CharField(max_length=255, default='')