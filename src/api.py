from django.views.decorators.csrf import csrf_exempt

from src.env import error400, error403
from src.settings import env, DEBUG
from src.views import result_json
from src.wrapper_1d import design_1d_run
from src.wrapper_2d import design_2d_run
from src.wrapper_3d import design_3d_run

import re


ALLOWED_ORIGIN = [env('ALLOWED_CORS_HOST')] if not DEBUG else [env('ALLOWED_CORS_HOST'), 'http://localhost:9000']

@csrf_exempt
def submit(request):
    if not ('HTTP_ORIGIN' in request.META and request.META.get('HTTP_ORIGIN') in ALLOWED_ORIGIN): return error403(request)

    if request.method != 'POST' or ('type' not in request.POST) or (request.POST.get('type') not in ('1', '2', '3')): return error400(request)

    job_type = int(request.POST.get('type'))
    if job_type == 1:
        response = design_1d_run(request)
    elif job_type == 2:
        response = design_2d_run(request)
    elif job_type == 3:
        response = design_3d_run(request)

    response['Access-Control-Allow-Origin'] = request.META.get('HTTP_ORIGIN')
    response['Access-Control-Allow-Methods'] =  'POST, OPTIONS'
    return response

def result(request):
    if request.method != 'GET': return error403(request)
    if 'job_id' not in request.GET: return error400(request)

    job_id = request.GET.get('job_id')
    if len(job_id) != 16 or (not re.match('[0-9a-fA-F]{16}', job_id)): return error400(request)
    response = result_json(job_id)
    response['Access-Control-Allow-Origin'] = request.META.get('HTTP_ORIGIN')
    response['Access-Control-Allow-Methods'] =  'GET'
    return response
