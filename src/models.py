from django.db import models
from django import forms
from django.utils.html import format_html

from src.settings import *

# import os


class Design1D(models.Model):
    date = models.DateField()
    job_id = models.CharField(blank=False, unique=True, max_length=16)
    sequence = models.TextField(blank=False)
    tag = models.CharField(blank=True, max_length=31)
    params = models.CharField(blank=True, max_length=255)
    status = models.CharField(blank=False, max_length=15)


class HistoryItem(models.Model):
    date = models.DateField()
    content_html = models.CharField(blank=False, max_length=1023)


class SourceDownloader(models.Model):
    date = models.DateField()
    first_name = models.CharField(blank=False, max_length=31)
    last_name = models.CharField(blank=False, max_length=31)
    institution = models.CharField(blank=False, max_length=31)
    department = models.CharField(blank=False, max_length=31)
    email = models.CharField(blank=False, max_length=255)
    is_subscribe = models.BooleanField(default=True)


class Design1DForm(forms.Form):
    sequence = forms.CharField(widget=forms.Textarea, required=True)
    tag = forms.CharField(required=False)
    min_Tm = forms.FloatField(required=False, min_value=10.0, max_value=100.0, initial=60.0)
    max_len = forms.IntegerField(required=False, min_value=60, initial=60)
    min_len = forms.IntegerField(required=False, min_value=0, initial=15)
    num_primers = forms.IntegerField(required=False, min_value=0, initial=0)
    is_num_primers = forms.BooleanField(required=False, initial=False)
    is_check_t7 = forms.BooleanField(required=False, initial=True)


class DownloadForm(forms.Form):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    institution = forms.CharField(required=True)
    department = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    is_subscribe = forms.BooleanField(initial=True, required=False)


def ga_tracker(request):
    return {'TRACKING_ID': GA['TRACKING_ID']}
