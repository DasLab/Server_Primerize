from django.http import HttpResponseRedirect, HttpResponse
#, HttpResponseBadRequest, HttpResponseNotFound, HttpResponseServerError
from django.template import RequestContext
# from django.contrib import messages
# from django.db import IntegrityError
# from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response


# from src.console import *
from src.helper import *
from src.models import *
from src.settings import *
from src.wrapper_1d import *

from datetime import datetime
import re
import simplejson


def index(request):
    return render_to_response(PATH.HTML_PATH['index'], {}, context_instance=RequestContext(request))

def tutorial(request):
    return render_to_response(PATH.HTML_PATH['tutorial'], {'job_id': ARG['DEMO_2D_ID']}, context_instance=RequestContext(request))

def protocol(request):
    return render_to_response(PATH.HTML_PATH['protocol'], {}, context_instance=RequestContext(request))

def license(request):
    return render_to_response(PATH.HTML_PATH['license'], {}, context_instance=RequestContext(request))

def docs(request):
    return render_to_response(PATH.HTML_PATH['docs'], {}, context_instance=RequestContext(request))

def about(request):
    history_list = HistoryItem.objects.order_by('-date')
    return render_to_response(PATH.HTML_PATH['about'], {'history': history_list}, context_instance=RequestContext(request))

def download(request):
    if request.method != 'POST':
        return render_to_response(PATH.HTML_PATH['download'], {'dl_form': DownloadForm(), 'flag': 0}, context_instance=RequestContext(request))
    else:
        flag = -1
        form = DownloadForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            inst = form.cleaned_data['institution']
            dept = form.cleaned_data['department']
            email = form.cleaned_data['email']
            is_valid = is_valid_name(first_name, "- ", 2) and is_valid_name(last_name, "- ", 1) and is_valid_name(inst, "()-, ", 4) and is_valid_name(dept, "()-, ", 4) and is_valid_email(email)
            if is_valid:
                user = SourceDownloader(date=datetime.now(), first_name=first_name, last_name=last_name, institution=inst, department=dept, email=email, is_subscribe=form.cleaned_data['is_subscribe'])
                user.save()
                flag = 1

        return render_to_response(PATH.HTML_PATH['download'], {'dl_form': form, 'flag': flag}, context_instance=RequestContext(request))


def result(request):
    if request.method == 'POST': return error400(request)
    if not request.GET.has_key('job_id'):
        return error404(request)
    else:
        job_id = request.GET['job_id']
        if not job_id: return HttpResponseRedirect('/')
        if len(job_id) != 16 or (not re.match('[0-9a-fA-F]{16}', job_id)): return error400(request)
        try:
            job_list_entry = JobIDs.objects.get(job_id=job_id)
        except:
            return error404(request)
        if job_list_entry.type == '1':
            job_entry = Design1D.objects.get(job_id=job_id)
            params = simplejson.loads(job_entry.params)
            form = Design1DForm(initial={'sequence': job_entry.sequence, 'tag': job_entry.tag, 'min_Tm': params['min_Tm'], 'max_len': params['max_len'], 'min_len': params['min_len'], 'num_primers': params['num_primers'], 'is_num_primers': params['is_num_primers'], 'is_check_t7': params['is_check_t7']})
            return render_to_response(PATH.HTML_PATH['design_1d'], {'1d_form': form, 'result_job_id': job_id}, context_instance=RequestContext(request))
        elif job_list_entry.type == '2':
            job_entry = Design2D.objects.get(job_id=job_id)
            params = simplejson.loads(job_entry.params)
            primers = job_entry.primers.replace('[', '').replace(']', '').replace("'", '').replace(' ', '')
            form = Design2DForm(initial={'sequence': job_entry.sequence, 'tag': job_entry.tag, 'primers': primers, 'max_muts': params['max_muts'], 'min_muts': params['min_muts'], 'offset': params['offset'], 'lib': str(params['which_lib'][0])})
            return render_to_response(PATH.HTML_PATH['design_2d'], {'2d_form': form, 'result_job_id': job_id}, context_instance=RequestContext(request))
        elif job_list_entry.type == '3':
            pass
        else:
            raise ValueError


def ping_test(request):
    return HttpResponse(content="", status=200)

def get_admin(request):
    return HttpResponse(simplejson.dumps({'email': EMAIL_NOTIFY}, sort_keys=True, indent=' ' * 4), content_type='application/json')

def get_user(request):
    if request.user.username: 
        user = request.user.username
    else:
        user = 'unknown'
    return HttpResponse(simplejson.dumps({'user': user}, sort_keys=True, indent=' ' * 4), content_type='application/json')

def get_js(request):
    lines = open('%s/cache/stat_sys.txt' % MEDIA_ROOT, 'r').readlines()
    lines = ''.join(lines).split('\t')
    json = {'jquery':lines[9], 'bootstrap':lines[10], 'd3':lines[14], 'zclip':lines[15]}
    return HttpResponse(simplejson.dumps(json, sort_keys=True, indent=' ' * 4), content_type='application/json')

def get_ver(request):
    lines = open('%s/cache/stat_sys.txt' % MEDIA_ROOT, 'r').readlines()
    lines = ''.join(lines).split('\t')
    json = {'primerize':lines[37]}
    return HttpResponse(simplejson.dumps(json, sort_keys=True, indent=' ' * 4), content_type='application/json')


def error400(request):
    return render_to_response(PATH.HTML_PATH['400'], {}, context_instance=RequestContext(request))
def error401(request):
    return render_to_response(PATH.HTML_PATH['401'], {}, context_instance=RequestContext(request))
def error403(request):
    return render_to_response(PATH.HTML_PATH['403'], {}, context_instance=RequestContext(request))
def error404(request):
    return render_to_response(PATH.HTML_PATH['404'], {}, context_instance=RequestContext(request))
def error500(request):
    return render_to_response(PATH.HTML_PATH['500'], {}, context_instance=RequestContext(request))
def error503(request):
    return render_to_response(PATH.HTML_PATH['503'], {}, context_instance=RequestContext(request))


def test(request):
    # print request.META
    raise ValueError
    return error400(request)
    # send_notify_emails('test', 'test')
    # send_mail('text', 'test', EMAIL_HOST_USER, [EMAIL_NOTIFY])
    return HttpResponse(content="", status=200)

