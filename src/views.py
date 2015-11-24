from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest, HttpResponseNotFound, HttpResponseServerError
from django.template import RequestContext#, Template
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import IntegrityError
# from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from django.shortcuts import render, render_to_response, redirect

from filemanager import FileManager

# from src.console import *
# from src.dash import *
from src.models import *
from src.settings import *

import re
import traceback


def index(request):
    return render_to_response(PATH.HTML_PATH['index'], {'tracking_id':GA['TRACKING_ID']}, context_instance=RequestContext(request))

def tutorial(request):
    return render_to_response(PATH.HTML_PATH['tutorial'], {'tracking_id':GA['TRACKING_ID']}, context_instance=RequestContext(request))

def protocol(request):
    return render_to_response(PATH.HTML_PATH['protocol'], {'tracking_id':GA['TRACKING_ID']}, context_instance=RequestContext(request))

def license(request):
    return render_to_response(PATH.HTML_PATH['license'], {'tracking_id':GA['TRACKING_ID']}, context_instance=RequestContext(request))

def about(request):
    lines = open(os.path.join(MEDIA_ROOT, 'cache/sys_hist.txt'), "r").readlines()
    script = "".join(lines).replace('#|#', '</i></td><td>').replace('#$#', '<tr><td><i>').replace('\n', '</td></tr>')
    return render_to_response(PATH.HTML_PATH['about'], {'tracking_id':GA['TRACKING_ID'], 'history':script}, context_instance=RequestContext(request))

def download(request):
    if request.method != 'POST':
        return render_to_response(PATH.HTML_PATH['download'], {'tracking_id':GA['TRACKING_ID']}, context_instance=RequestContext(request))
    else:
        form = DownloadForm(request.POST)
        if form.is_valid():
            print form.__str__, dict(form)



def design_1d(request):
    return render_to_response(PATH.HTML_PATH['design_1d'], {'tracking_id':GA['TRACKING_ID']}, context_instance=RequestContext(request))


def ping_test(request):
    return HttpResponse(content="", status=200)

def get_admin(request):
    return HttpResponse(simplejson.dumps({'email':EMAIL_NOTIFY}), content_type='application/json')

def get_js(request):
    lines = open('%s/cache/stat_sys.txt' % MEDIA_ROOT, 'r').readlines()
    lines = ''.join(lines).split('\t')
    json = {'jquery':lines[11], 'bootstrap':lines[12]}
    return HttpResponse(simplejson.dumps(json), content_type='application/json')


def error400(request):
    return render_to_response(PATH.HTML_PATH['400'], {}, context_instance=RequestContext(request))
def error401(request):
    return render_to_response(PATH.HTML_PATH['401'], {}, context_instance=RequestContext(request))
def error403(request):
    return render_to_response(PATH.HTML_PATH['403'], {}, context_instance=RequestContext(request))
def error404(request):
    return render_to_response(PATH.HTML_PATH['404'], {'tracking_id':GA['TRACKING_ID']}, context_instance=RequestContext(request))
def error500(request):
    return render_to_response(PATH.HTML_PATH['500'], {}, context_instance=RequestContext(request))


def test(request):
    print request.META
    raise ValueError
    return error400(request)
    # send_notify_emails('test', 'test')
    # send_mail('text', 'test', EMAIL_HOST_USER, [EMAIL_NOTIFY])
    return HttpResponse(content="", status=200)

