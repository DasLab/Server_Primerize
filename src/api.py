from django.views.decorators.csrf import csrf_exempt

from src.env import error400, error403
from src.wrapper_1d import design_1d_run
from src.wrapper_2d import design_2d_run
from src.wrapper_3d import design_3d_run


@csrf_exempt
def submit(request):
    if 'type' not in request.POST: return error400(request)

    job_type = request.POST.get('type')
    if job_type == 1:
        return design_1d_run(request)
    elif job_type == 2:
        return design_2d_run(request)
    elif job_type == 3:
        return design_3d_run(request)
    return error400(request)
