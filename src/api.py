from django.views.decorators.csrf import csrf_exempt

from src.env import error400, error403
from src.settings import env, DEBUG
from src.wrapper_1d import design_1d_run
from src.wrapper_2d import design_2d_run
from src.wrapper_3d import design_3d_run


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
