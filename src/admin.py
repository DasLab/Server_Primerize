from django.contrib import admin
from django.utils.html import format_html
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.core.management import call_command

from src.console import *
from src.models import *
from src.settings import *

UserAdmin.list_display = ('username', 'email', 'last_login', 'is_active', 'is_staff', 'is_superuser')
UserAdmin.ordering = ('-is_superuser', '-is_staff', 'username')
# admin.site.unregister(User)
admin.site.register(User, UserAdmin)


class JobIDsAdmin(admin.ModelAdmin):
    list_display = ('date', 'job_id', 'type',)
    ordering = ('-date', '-job_id',)
    fieldsets = [
        (format_html('<span class="glyphicon glyphicon-info-sign"></span>&nbsp;Entry'), {'fields': ['date', ('job_id', 'type')]}),
    ]
admin.site.register(JobIDs, JobIDsAdmin)

class JobGroupsAdmin(admin.ModelAdmin):
    list_display = ('id', 'tag', 'job_1d', 'job_2d', 'job_3d',)
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
    list_display = ('date', 'job_id', 'tag', 'status', 'sequence',)
    ordering = ('-date',)
    fieldsets = [
        (format_html('<span class="glyphicon glyphicon-info-sign"></span>&nbsp;Entry'), {'fields': ['date', ('job_id', 'tag'), 'sequence', 'primers', 'params']}),
        (format_html('<span class="glyphicon glyphicon-exclamation-sign"></span>&nbsp;Results'), {'fields': [('status', 'time'), 'plates']}),
    ]
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
        (format_html('<span class="glyphicon glyphicon-user"></span>&nbsp;Personal Information'), {'fields': [ 'date', ('first_name', 'last_name'), ('institution', 'department'), 'email', 'is_subscribe']}),
    ]
admin.site.register(SourceDownloader, SourceDownloaderAdmin)


############################################################################################################################################

def sys_stat(request):
    call_command('versions')
    return HttpResponseRedirect('/admin/')

def backup_stat(request):
    get_backup_stat()
    return HttpResponseRedirect('/admin/backup/')

def backup_form(request):
    return HttpResponse(simplejson.dumps(get_backup_form()), content_type='application/json')

def backup_now(request):
    call_command('backup')
    return backup_stat(request)

def upload_now(request):
    call_command('gdrive')
    return backup_stat(request)


def apache_stat(request):
    return HttpResponse(restyle_apache(), content_type='application/json')

def apache(request):
    return render_to_response(PATH.HTML_PATH['admin_apache'], {'host_name': env('SSL_HOST')}, context_instance=RequestContext(request))


def aws(request):
    return render_to_response(PATH.HTML_PATH['admin_aws'], {'timezone': TIME_ZONE}, context_instance=RequestContext(request))

def aws_stat(request):
    json = aws_stats(request)
    if isinstance(json, HttpResponse): return json
    return HttpResponse(json, content_type='application/json')

def ga(request):
    return render_to_response(PATH.HTML_PATH['admin_ga'], {'ga_url': GA['LINK_URL']}, context_instance=RequestContext(request))

def ga_stat(request):
    json = ga_stats(request)
    if isinstance(json, HttpResponse): return json
    return HttpResponse(json, content_type='application/json')

def git(request):
    return render_to_response(PATH.HTML_PATH['admin_git'], {'timezone': TIME_ZONE, 'git_repo': GIT['REPOSITORY']}, context_instance=RequestContext(request))

def git_stat(request):
    json = git_stats(request)
    if isinstance(json, HttpResponse): return json
    return HttpResponse(json, content_type='application/json')


def backup(request):
    flag = -1
    if request.method == 'POST':
        flag = set_backup_form(request)

    form = BackupForm(initial=get_backup_form())
    return render_to_response(PATH.HTML_PATH['admin_backup'], {'form': form, 'flag': flag, 'email': EMAIL_HOST_USER}, context_instance=RequestContext(request))

def dir(request):
    return render_to_response(PATH.HTML_PATH['admin_dir'], {}, context_instance=RequestContext(request))

def doc(request):
    return render_to_response(PATH.HTML_PATH['admin_doc'], {}, context_instance=RequestContext(request))

def man(request):
    return render_to_response(PATH.HTML_PATH['admin_man'], {}, context_instance=RequestContext(request))

def ref(request):
    return render_to_response(PATH.HTML_PATH['admin_ref'], {}, context_instance=RequestContext(request))


def get_ver(request):
    stats = simplejson.load(open('%s/cache/stat_ver.json' % MEDIA_ROOT, 'r'))
    return HttpResponse(simplejson.dumps(stats, sort_keys=True, indent=' ' * 4), content_type='application/json')

def get_sys(request):
    stats = simplejson.load(open('%s/cache/stat_sys.json' % MEDIA_ROOT, 'r'))
    return HttpResponse(simplejson.dumps(stats, sort_keys=True, indent=' ' * 4), content_type='application/json')

def get_backup(request):
    stats = simplejson.load(open('%s/cache/stat_backup.json' % MEDIA_ROOT, 'r'))
    return HttpResponse(simplejson.dumps(stats, sort_keys=True, indent=' ' * 4), content_type='application/json')


admin.site.register_view('backup/', view=backup, visible=False)
admin.site.register_view('backup_stat/', view=backup_stat, visible=False)
admin.site.register_view('backup_form/', view=backup_form, visible=False)
admin.site.register_view('backup_now/', view=backup_now, visible=False)
admin.site.register_view('upload_now/', view=upload_now, visible=False)

admin.site.register_view('apache_stat/', view=apache_stat, visible=False)
admin.site.register_view('apache/', view=apache, visible=False)

admin.site.register_view('aws/', view=aws, visible=False)
admin.site.register_view('aws_stat/', view=aws_stat, visible=False)

admin.site.register_view('ga/', view=ga, visible=False)
admin.site.register_view('ga_stat/', view=ga_stat, visible=False)

admin.site.register_view('git/', view=git, visible=False)
admin.site.register_view('git_stat/', view=git_stat, visible=False)

admin.site.register_view('dir/', view=dir, visible=False)
admin.site.register_view('doc/', view=doc, visible=False)
admin.site.register_view('man/', view=man, visible=False)
admin.site.register_view('ref/', view=ref, visible=False)

admin.site.register_view('sys_stat/', view=sys_stat, visible=False)
admin.site.register_view('get_ver/', view=get_ver, visible=False)
admin.site.register_view('get_sys/', view=get_sys, visible=False)
admin.site.register_view('get_backup/', view=get_backup, visible=False)
