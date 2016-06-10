from django.contrib import admin
from django.utils.html import format_html
from django.shortcuts import render
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
    list_display = ('date', 'job_id', 'tag', 'status', 'sequence',)
    ordering = ('-date',)
    fieldsets = [
        (format_html('<span class="glyphicon glyphicon-info-sign"></span>&nbsp;Entry'), {'fields': ['date', ('job_id', 'tag'), 'sequence', 'structures', 'primers', 'params']}),
        (format_html('<span class="glyphicon glyphicon-exclamation-sign"></span>&nbsp;Results'), {'fields': [('status', 'time'), 'plates']}),
    ]
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

def backup_form(request):
    return HttpResponse(simplejson.dumps(get_backup_form(), sort_keys=True, indent=' ' * 4), content_type='application/json')

def admin_cmd(request, keyword):
    call_command(keyword.strip('/'))
    return refresh_stat(request, 'backup')


def apache(request):
    return render(request, PATH.HTML_PATH['admin_apache'], {'host_name': env('SSL_HOST')})

def aws(request):
    return render(request, PATH.HTML_PATH['admin_aws'], {'timezone': TIME_ZONE})

def ga(request):
    return render(request, PATH.HTML_PATH['admin_ga'], {'ga_url': GA['LINK_URL']})

def git(request):
    return render(request, PATH.HTML_PATH['admin_git'], {'timezone': TIME_ZONE, 'git_repo': GIT['REPOSITORY']})


def backup(request):
    flag = -1
    if request.method == 'POST':
        flag = set_backup_form(request)

    form = BackupForm(initial=get_backup_form())
    return render(request, PATH.HTML_PATH['admin_backup'], {'form': form, 'flag': flag, 'email': EMAIL_HOST_USER})

def dir(request):
    return render(request, PATH.HTML_PATH['admin_dir'])

def doc(request):
    return render(request, PATH.HTML_PATH['admin_doc'])

def man(request):
    return render(request, PATH.HTML_PATH['admin_man'])

def ref(request):
    return render(request, PATH.HTML_PATH['admin_ref'])


def get_stat(request, keyword):
    if keyword == "arch":
        return HttpResponse(''.join(open('%s/config/flow_chart.svg' % MEDIA_ROOT).readlines()), content_type='image/svg+xml')
    json = simplejson.load(open('%s/cache/stat_%s.json' % (MEDIA_ROOT, keyword.strip('/')), 'r'))
    return HttpResponse(simplejson.dumps(json, sort_keys=True, indent=' ' * 4), content_type='application/json')

def refresh_stat(request, keyword):
    keyword = keyword.strip('/')
    if keyword == 'sys':
        call_command('versions')
        return HttpResponseRedirect('/admin/')
    elif keyword == 'backup':
        get_backup_stat()
        return HttpResponseRedirect('/admin/backup/')

def get_dash(request, keyword):
    if keyword == 'apache':
        json = restyle_apache()
    elif keyword == 'aws':
        json = aws_stats(request)
    elif keyword == 'ga':
        json = ga_stats(request)
    elif keyword == 'git':
        json = git_stats(request)

    if isinstance(json, HttpResponse): return json
    return HttpResponse(json, content_type='application/json')


admin.site.register_view('backup/', view=backup, visible=False)
admin.site.register_view('backup/form/', view=backup_form, visible=False)
admin.site.register_view(r'cmd/(upload|backup)/?$', view=admin_cmd, visible=False)

admin.site.register_view('apache/', view=apache, visible=False)
admin.site.register_view('aws/', view=aws, visible=False)
admin.site.register_view('ga/', view=ga, visible=False)
admin.site.register_view('git/', view=git, visible=False)

admin.site.register_view('dir/', view=dir, visible=False)
admin.site.register_view('cherrypy/', view=doc, visible=False)
admin.site.register_view('man/', view=man, visible=False)
admin.site.register_view('ref/', view=ref, visible=False)


admin.site.register_view(r'dash/(apache|aws|ga|git)/?$', view=get_dash, visible=False)
admin.site.register_view(r'stat/(ver|sys|backup|arch)/?$', view=get_stat, visible=False)
admin.site.register_view(r'stat/(sys|backup)/refresh/?$', view=refresh_stat, visible=False)
