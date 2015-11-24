from django.db import models
from django import forms
from django.utils.html import format_html

from src.settings import *

# import os


class SourceDownloader(models.Model):
    date = models.DateField()
    first_name = models.CharField(blank=False, max_length=31)
    last_name = models.CharField(blank=False, max_length=31)
    institution = models.CharField(blank=False, max_length=31)
    department = models.CharField(blank=False, max_length=31)
    email = models.CharField(blank=False, max_length=255)
    is_subscribe = models.BooleanField(default=True)


class DownloadForm(forms.Form):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    institution = forms.CharField(required=True)
    department = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    is_subscribe = forms.BooleanField(initial=True)