from django.contrib import admin
from django.forms import ModelForm, widgets, DateField, DateInput
from django.utils.html import format_html
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
# from django.contrib.admin import AdminSite
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from datetime import datetime
import time

from src.console import *
from src.models import *
from src.settings import *

UserAdmin.list_display = ('username', 'email', 'last_login', 'is_active', 'is_staff', 'is_superuser')
UserAdmin.ordering = ('-is_superuser', '-is_staff', 'username')
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


class JobIDsAdmin(admin.ModelAdmin):
    list_display = ('job_id', 'type',)
    ordering = ('-job_id',)
    fieldsets = [
        (format_html('<span class="glyphicon glyphicon-info-sign"></span>&nbsp;Entry'), {'fields': [('job_id', 'type')]}),
    ]
admin.site.register(JobIDs, JobIDsAdmin)

class JobGroupsAdmin(admin.ModelAdmin):
    list_display = ('tag', 'job_1d', 'job_2d', 'job_3d',)
    # ordering = ('-job_id',)
    fieldsets = [
        (format_html('<span class="glyphicon glyphicon-info-sign"></span>&nbsp;Entry'), {'fields': ['tag', 'job_1d', 'job_2d', 'job_3d']}),
    ]
admin.site.register(JobGroups, JobGroupsAdmin)


class Design1DAdmin(admin.ModelAdmin):
    list_display = ('date', 'job_id', 'tag', 'status', 'sequence',)
    ordering = ('-date',)
    fieldsets = [
        (format_html('<span class="glyphicon glyphicon-info-sign"></span>&nbsp;Entry'), {'fields': ['date', ('job_id', 'tag'), 'sequence', 'params']}),
        (format_html('<span class="glyphicon glyphicon-exclamation-sign"></span>&nbsp;Results'), {'fields': [('status', 'time'), 'primers']}),
    ]
admin.site.register(Design1D, Design1DAdmin)

class Design2DAdmin(admin.ModelAdmin):
    pass
admin.site.register(Design2D, Design2DAdmin)

class Design3DAdmin(admin.ModelAdmin):
    pass
admin.site.register(Design3D, Design3DAdmin)


class HistoryItemAdmin(admin.ModelAdmin):
    list_display = ('date', 'content_html',)
    ordering = ('-date',)
    fieldsets = [
        (format_html('<span class="glyphicon glyphicon-comment"></span>&nbsp;Contents'), {'fields': ['date', 'content_html']}),
    ]
admin.site.register(HistoryItem, HistoryItemAdmin)

class SourceDownloaderAdmin(admin.ModelAdmin):
    list_display = ('date', 'full_name', 'affiliation', 'email')
    ordering = ('-date', 'last_name',)

    fieldsets = [
        (format_html('<span class="glyphicon glyphicon-user"></span>&nbsp;Personal Information'), {'fields': [('first_name', 'last_name'), ('institution', 'department'), 'email', 'is_subscribe']}),
    ]
admin.site.register(SourceDownloader, SourceDownloaderAdmin)


############################################################################################################################################

def sys_stat(request):
    sys_ver_weekly()
    return HttpResponseRedirect('/admin')
admin.site.register_view('sys_stat', view=sys_stat, visible=False)

def backup_stat(request):
    get_backup_stat()
    return HttpResponseRedirect('/admin/backup')
admin.site.register_view('backup_stat', view=backup_stat, visible=False)

def backup_form(request):
    return HttpResponse(get_backup_form(), content_type='application/json')
admin.site.register_view('backup_form', view=backup_form, visible=False)

def backup_now(request):
    backup_weekly()
    return backup_stat(request)
admin.site.register_view('backup_now', view=backup_now, visible=False)

def upload_now(request):
    gdrive_weekly()
    return backup_stat(request)
admin.site.register_view('upload_now', view=upload_now, visible=False)


def apache_stat(request):
    return HttpResponse(restyle_apache(), content_type='application/json')
admin.site.register_view('apache_stat', view=apache_stat, visible=False)

def apache(request):
    return render_to_response(PATH.HTML_PATH['admin_apache'], {}, context_instance=RequestContext(request))
admin.site.register_view('apache/', view=apache, visible=False)


def aws(request):
    return render_to_response(PATH.HTML_PATH['admin_aws'], {'timezone':TIME_ZONE}, context_instance=RequestContext(request))
admin.site.register_view('aws/', view=aws, visible=False)

def aws_stat(request):
    json = aws_stats(request)
    if isinstance(json, HttpResponseBadRequest): return json
    return HttpResponse(json, content_type='application/json')
admin.site.register_view('aws_stat', view=aws_stat, visible=False)

def aws_admin(request):
    json = ga_stats()
    if isinstance(json, HttpResponseBadRequest): return json
    return HttpResponse(json, content_type='application/json')
admin.site.register_view('aws_admin', view=aws_admin, visible=False)

def ga(request):
    return render_to_response(PATH.HTML_PATH['admin_ga'], {}, context_instance=RequestContext(request))
admin.site.register_view('ga/', view=ga, visible=False)

def ga_admin(request):
    json = ga_stats()
    if isinstance(json, HttpResponseBadRequest): return json
    return HttpResponse(json, content_type='application/json')
admin.site.register_view('ga_admin', view=ga_admin, visible=False)

def git(request):
    return render_to_response(PATH.HTML_PATH['admin_git'], {'timezone':TIME_ZONE, 'git_repo':GIT['REPOSITORY']}, context_instance=RequestContext(request))
admin.site.register_view('git/', view=git, visible=False)

def git_stat(request):
    json = git_stats(request)
    if isinstance(json, HttpResponseBadRequest):
        return json
    elif isinstance(json, HttpResponseServerError):
        i = 0
        while (isinstance(json, HttpResponseServerError) and i <= 5):
            i += 1
            time.sleep(1)
            json = git_stats(request)
        if isinstance(json, HttpResponseServerError): return json
    return HttpResponse(json, content_type='application/json')
admin.site.register_view('git_stat', view=git_stat, visible=False)

def ssl_dash(request):
    return HttpResponse(dash_ssl(request), content_type='application/json')
admin.site.register_view('ssl_dash', view=ssl_dash, visible=False)


def backup(request):
    flag = 0
    if request.method == 'POST':
        set_backup_form(request)
        flag = 1
    lines = open('%s/config/cron.conf' % MEDIA_ROOT, 'r').readlines()

    index =  [i for i, line in enumerate(lines) if 'KEEP_BACKUP' in line][0]
    keep = int(lines[index].split(':')[1])
    return render_to_response(PATH.HTML_PATH['admin_backup'], {'form':BackupForm(), 'flag':flag, 'keep':keep, 'email':EMAIL_HOST_USER}, context_instance=RequestContext(request))
admin.site.register_view('backup/', view=backup, visible=False)

def dir(request):
    return render_to_response(PATH.HTML_PATH['admin_dir'], {}, context_instance=RequestContext(request))
admin.site.register_view('dir/', view=dir, visible=False)

def doc(request):
    return render_to_response(PATH.HTML_PATH['admin_doc'], {}, context_instance=RequestContext(request))
admin.site.register_view('doc/', view=doc, visible=False)


def get_ver(request):
    lines = open('%s/cache/stat_sys.txt' % MEDIA_ROOT, 'r').readlines()
    lines = ''.join(lines)
    return HttpResponse(lines, content_type='text/plain')
admin.site.register_view('get_ver/', view=get_ver, visible=False)

def get_backup(request):
    lines = open('%s/cache/stat_backup.txt' % MEDIA_ROOT, 'r').readlines()
    lines = ''.join(lines)
    return HttpResponse(lines, content_type='text/plain')
admin.site.register_view('get_backup/', view=get_backup, visible=False)

