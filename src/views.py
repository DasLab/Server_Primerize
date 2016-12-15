from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.utils.encoding import smart_str

from src.console import *
from src.env import error400, error401, error403, error404, error500, error503
from src.helper_form import is_valid_name, is_valid_email
from src.models import *
from src.settings import *

from datetime import datetime
import re
import simplejson
import traceback


def index(request):
    return render(request, PATH.HTML_PATH['index'])

def tutorial(request):
    return render(request, PATH.HTML_PATH['tutorial'], {'job_id_2d': ARG['DEMO_2D_ID'], 'job_id_3d': ARG['DEMO_3D_ID_2']})

def protocol(request):
    return render(request, PATH.HTML_PATH['protocol'])

def docs(request):
    return render(request, PATH.HTML_PATH['docs'])

def about(request):
    history_list = HistoryItem.objects.order_by('-date')
    return render(request, PATH.HTML_PATH['about'], {'history': history_list})

def landing(request):
    return render(request, PATH.HTML_PATH['landing'])


def license(request):
    license_md = ''.join(open('%s/dist/Primerize-LICENSE.md' % MEDIA_ROOT, 'r').readlines())
    license_md = license_md.replace('\n', '<br/>') + '</strong>'
    return render(request, PATH.HTML_PATH['license'], {'license_md': license_md})

def download(request):
    if request.method != 'POST':
        result = simplejson.load(open('%s/cache/stat_dist.json' % MEDIA_ROOT, 'r'))
        return render(request, PATH.HTML_PATH['download'], {'dl_form': DownloadForm(), 'dist': result})
    else:
        (flag, msg) = (0, '')
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
            else:
                msg += '' if is_valid_name(first_name, "- ", 2) else '<li>Invalid <u>First Name</u>: only letters, numbers, and "-" allowed, and with minimum length 3 charaters required.</li>'
                msg += '' if is_valid_name(last_name, "- ", 1) else '<li>Invalid <u>Last Name</u>: only letters, numbers, and "-" allowed, with minimum length 2 charaters required.</li>'
                msg += '' if is_valid_name(inst, "()-, ", 4) else '<li>Invalid <u>Institution</u>: only letters, numbers, and "()-, " allowed, with minimum length 5 charaters required.</li>'
                msg += '' if is_valid_name(dept, "()-, ", 4) else '<li>Invalid <u>Department</u>: only letters, numbers, and "()-, " allowed, with minimum length 5 charaters required.</li>'
                msg += '' if is_valid_email(email) else '<li>Invalid <u>E-mail Address</u>.</li>'
        else:
            msg = 'Required form field(s) are missing.</li>'
        return HttpResponse(simplejson.dumps({'status': flag, 'message': msg}, sort_keys=True, indent=' ' * 4), content_type='application/json')

def link(request, tag):
    if not tag: return error400(request)

    if 'first_name' in request.GET and 'last_name' in request.GET and 'email' in request.GET:
        first_name = request.GET.get('first_name')
        last_name = request.GET.get('last_name')
        email = request.GET.get('email')
        records = SourceDownloader.objects.filter(first_name=first_name, last_name=last_name, email=email)
        if len(records):
            tag = tag.replace('/', '')
            file_name = '%s/dist/Primerize-%s.zip' % (MEDIA_ROOT, tag)
            if os.path.exists(file_name):
                response = HttpResponse(content_type='application/zip')
                response['Content-Disposition'] = 'attachment; filename=Primerize-%s.zip' % tag
                response['X-Sendfile'] = smart_str(file_name)
                return response
            else:
                return error404(request)
    return error401(request)


def result(request):
    if request.method == 'POST': return error403(request)

    if 'job_id' not in request.GET:
        return error400(request)
    else:
        job_id = request.GET.get('job_id')
        if not job_id: return HttpResponseRedirect('/')
        if len(job_id) != 16 or (not re.match('[0-9a-fA-F]{16}', job_id)): return error400(request)

        if 'json' in request.GET and request.GET.get('json').lower() != 'false': return result_json(job_id)
        try:
            job_list_entry = JobIDs.objects.get(job_id=job_id)
        except:
            return error404(request)
        form = Design1DForm() if job_list_entry.type == "1" else (Design2DForm() if job_list_entry.type == "2" else Design3DForm())
        json = {'result_job_id': job_id, '%sd_form' % job_list_entry.type: form}
        return render(request, PATH.HTML_PATH['design_%sd' % job_list_entry.type], json)

def result_json(job_id):
    try:
        job_list_entry = JobIDs.objects.get(job_id=job_id)
    except Exception:
        print '\033[41mERROR\033[0m: unmatched JobID: \033[92m%s\033[0m.' % job_id
        return HttpResponse(simplejson.dumps({'status': 404, 'error': 'JOB_ID not found'}, sort_keys=True, indent=' ' * 4), content_type='application/json')

    json = {'job_id': job_id, 'type': int(job_list_entry.type)}
    json_data = {}
    if job_list_entry.type == '1':
        job_entry = Design1D.objects.get(job_id=job_id)
    elif job_list_entry.type == '2':
        job_entry = Design2D.objects.get(job_id=job_id)
    elif job_list_entry.type == '3':
        job_entry = Design3D.objects.get(job_id=job_id)
        json_data.update({'structures': simplejson.loads(job_entry.structures)})
    else:
        raise ValueError

    json_data.update({'sequence': job_entry.sequence, 'tag': job_entry.tag, 'params': simplejson.loads(job_entry.params)})
    json.update({'status': int(job_entry.status), 'data': json_data, 'result': simplejson.loads(job_entry.result), 'time': round(job_entry.time, 2)})

    return HttpResponse(simplejson.dumps(json, sort_keys=True, indent=' ' * 4), content_type='application/json')


def ping_test(request):
    return HttpResponse(content="", status=200)


def get_staff(request):
    user = request.user.username if request.user.username else 'unknown'
    return HttpResponse(simplejson.dumps({'user': user, 'admin': EMAIL_NOTIFY}, sort_keys=True, indent=' ' * 4), content_type='application/json')


def test(request):
    # print request.META
    raise ValueError
    return error400(request)
    # send_notify_emails('test', 'test')
    # send_mail('text', 'test', EMAIL_HOST_USER, [EMAIL_NOTIFY])
    return HttpResponse(content="", status=200)

