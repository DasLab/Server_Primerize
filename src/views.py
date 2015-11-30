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
from src.helper import *
from src.models import *
from src.settings import *
from src.wrapper import *

from datetime import datetime
import re
import simplejson
import threading
import traceback


def index(request):
    return render_to_response(PATH.HTML_PATH['index'], {}, context_instance=RequestContext(request))

def tutorial(request):
    return render_to_response(PATH.HTML_PATH['tutorial'], {}, context_instance=RequestContext(request))

def protocol(request):
    return render_to_response(PATH.HTML_PATH['protocol'], {}, context_instance=RequestContext(request))

def license(request):
    return render_to_response(PATH.HTML_PATH['license'], {}, context_instance=RequestContext(request))

def about(request):
    history_list = HistoryItem.objects.order_by('-date')
    return render_to_response(PATH.HTML_PATH['about'], {'history':history_list}, context_instance=RequestContext(request))

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
                user = SourceDownloader(date=datetime.utcnow(), first_name=first_name, last_name=last_name, institution=inst, department=dept, email=email, is_subscribe=form.cleaned_data['is_subscribe'])
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
        if job_list_entry.type == 1:
            job_entry = Design1D.objects.get(job_id=job_id)
            params = simplejson.loads(job_entry.params)
            form = Design1DForm(initial={'sequence': job_entry.sequence, 'tag': job_entry.tag, 'min_Tm': params['min_Tm'], 'max_len': params['max_len'], 'min_len': params['min_len'], 'num_primers': params['num_primers'], 'is_num_primers': params['is_num_primers'], 'is_check_t7': params['is_check_t7']})
            return render_to_response(PATH.HTML_PATH['design_1d'], {'1d_form': form, 'result_job_id': job_id}, context_instance=RequestContext(request))
        elif job_list_entry.type == 2:
            pass
        elif job_list_entry.type == 3:
            pass
        else:
            raise ValueError


def design_1d(request):
    return render_to_response(PATH.HTML_PATH['design_1d'], {'1d_form': Design1DForm()}, context_instance=RequestContext(request))

def design_1d_run(request):
    if request.method != 'POST': return error400(request)
    form = Design1DForm(request.POST)
    if form.is_valid():
        sequence = form.cleaned_data['sequence']
        tag = form.cleaned_data['tag']
        min_Tm = form.cleaned_data['min_Tm']
        max_len = form.cleaned_data['max_len']
        min_len = form.cleaned_data['min_len']
        num_primers = form.cleaned_data['num_primers']
        is_num_primers = form.cleaned_data['is_num_primers']
        is_check_t7 = form.cleaned_data['is_check_t7']

        sequence = re.sub('[^' + ''.join(SEQ['valid']) + ']', '', sequence.upper().replace('U', 'T'))
        if not tag: tag = 'primer'
        if not min_Tm: min_Tm = ARG['MIN_TM']
        if not max_len: max_len = ARG['MAX_LEN']
        if not min_len: min_len = ARG['MIN_LEN']
        if (not num_primers) or (not is_num_primers): num_primers = ARG['NUM_PRM']

        msg = ''
        if len(sequence) < 60:
            msg = 'Invalid sequence input (should be <u>at least <b>60</b> nt</u> long and without illegal characters).'
        elif num_primers % 2:
            msg = 'Invalid advanced options input: <b>#</b> number of primers must be <b><u>EVEN</u></b>.'
        if msg:
            return HttpResponse(simplejson.dumps({'error': msg}), content_type='application/json')

        job_id = random_job_id()
        create_wait_html(job_id)
        job_entry = Design1D(date=datetime.utcnow(), job_id=job_id, sequence=sequence, tag=tag, status='1', params=simplejson.dumps({'min_Tm': min_Tm, 'max_len': max_len, 'min_len': min_len, 'num_primers': num_primers, 'is_num_primers': is_num_primers, 'is_check_t7': is_check_t7}))
        job_entry.save()
        job_list_entry = JobIDs(job_id=job_id, type=1)
        job_list_entry.save()
        job = threading.Thread(target=design_1d_wrapper, args=(sequence, tag, min_Tm, num_primers, max_len, min_len, is_check_t7, job_id))
        job.start()

        return HttpResponse(simplejson.dumps({'status': 'underway', 'job_id': job_id, 'sequence': sequence, 'tag': tag, 'min_Tm': min_Tm, 'max_len': max_len, 'min_len': min_len, 'num_primers': num_primers, 'is_num_primers': is_num_primers, 'is_check_t7': is_check_t7}), content_type='application/json')
    else:
        return HttpResponse(simplejson.dumps({'error': 'Invalid primary and/or advanced options input.'}), content_type='application/json')
    return render_to_response(PATH.HTML_PATH['design_1d'], {'1d_form': form}, context_instance=RequestContext(request))


def demo_1d(request):
    return HttpResponseRedirect('/result/?job_id=' + ARG['DEMO_1D_ID'])

def demo_1d_run(request):
    job_id = ARG['DEMO_1D_ID']
    create_wait_html(job_id)
    job = threading.Thread(target=design_1d_wrapper, args=(SEQ['P4P6'], 'P4P6_2HP', ARG['MIN_TM'], ARG['NUM_PRM'], ARG['MAX_LEN'], ARG['MIN_LEN'], 1, job_id))
    job.start()
    return HttpResponse(simplejson.dumps({'status': 'underway', 'job_id': job_id, 'sequence': SEQ['P4P6'], 'tag': 'P4P6_2HP', 'min_Tm': ARG['MIN_TM'], 'max_len': ARG['MAX_LEN'], 'min_len': ARG['MIN_LEN'], 'num_primers': ARG['NUM_PRM'], 'is_num_primers': 0, 'is_check_t7': 1}), content_type='application/json')



def user_login(request):
    if request.user.is_authenticated():
        if request.GET.has_key('next') and 'admin' in request.GET['next']:
            return error403(request)
        return HttpResponseRedirect('/')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        messages = 'Invalid username and/or password. Please try again.'
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            flag = form.cleaned_data['flag']
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    if flag == "Admin":
                        return HttpResponseRedirect('/admin')
                    else:
                        return HttpResponseRedirect('/')
                else:
                    messages = 'Inactive/disabled account. Please contact us.'
        return render_to_response(PATH.HTML_PATH['login'], {'form': form, 'messages': messages}, context_instance=RequestContext(request))
    else:
        if request.GET.has_key('next') and 'admin' in request.GET['next']:
            flag = 'Admin'
        else:
            flag = 'Member'
        form = LoginForm(initial={'flag': flag})
        return render_to_response(PATH.HTML_PATH['login'], {'form': form}, context_instance=RequestContext(request))

@login_required
def user_password(request):
    if request.method == 'POST':
        form = PasswordForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password_old = form.cleaned_data['password_old']
            password_new = form.cleaned_data['password_new']
            password_new_rep = form.cleaned_data['password_new_rep']
            if password_new != password_new_rep:
                return render_to_response(PATH.HTML_PATH['password'], {'form': form, 'messages': 'New password does not match. Please try again.'}, context_instance=RequestContext(request))
            if password_new == password_old:
                return render_to_response(PATH.HTML_PATH['password'], {'form': form, 'messages': 'New password is the same as current. Please try again.'}, context_instance=RequestContext(request))

            user = authenticate(username=username, password=password_old)
            if user is not None:
                u = User.objects.get(username=username)
                u.set_password(password_new)
                u.save()
                logout(request)
                return render_to_response(PATH.HTML_PATH['password'], {'form': form, 'notices': 'Password change successful. Please sign in using new credentials.'}, context_instance=RequestContext(request))
        form = PasswordForm(initial={'username': request.user.username})
        return render_to_response(PATH.HTML_PATH['password'], {'form': form, 'messages': 'Invalid username and/or current password, or missing new password.<br/>Please try again.'}, context_instance=RequestContext(request))
    else:
        form = PasswordForm(initial={'username': request.user.username})
        return render_to_response(PATH.HTML_PATH['password'], {'form': form}, context_instance=RequestContext(request))

def user_logout(request):
    logout(request)
    return HttpResponseRedirect("/")


@user_passes_test(lambda u: u.is_superuser)
def browse(request, path):
    fm = FileManager(MEDIA_ROOT + '/data')
    return fm.render(request, path)


def ping_test(request):
    return HttpResponse(content="", status=200)

def get_admin(request):
    return HttpResponse(simplejson.dumps({'email': EMAIL_NOTIFY}), content_type='application/json')

def get_user(request):
    if request.user.username: 
        user = request.user.username
    else:
        user = 'unknown'
    return HttpResponse(simplejson.dumps({'user': user}), content_type='application/json')

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
    return render_to_response(PATH.HTML_PATH['404'], {}, context_instance=RequestContext(request))
def error500(request):
    return render_to_response(PATH.HTML_PATH['500'], {}, context_instance=RequestContext(request))


def test(request):
    print request.META
    raise ValueError
    return error400(request)
    # send_notify_emails('test', 'test')
    # send_mail('text', 'test', EMAIL_HOST_USER, [EMAIL_NOTIFY])
    return HttpResponse(content="", status=200)

