from django.http import HttpResponseRedirect, HttpResponse
#, HttpResponseBadRequest, HttpResponseNotFound, HttpResponseServerError
from django.shortcuts import render

from datetime import datetime
import simplejson
import sys
import threading
import time
import traceback

from src.helper import *
from src.helper_form import *
from src.helper_html import *
from src.models import *
from src.views import result_json, error400


def design_3d(request, form=Design3DForm(), from_1d=False, from_2d=False):
    return render(request, PATH.HTML_PATH['design_3d'], {'3d_form': form, 'from_1d': from_1d, 'from_2d': from_2d})

def design_3d_run(request):
    if request.method != 'POST': return error400(request)
    form = Design3DForm(request.POST)
    msg = ''
    if form.is_valid():
        (sequence, tag) = form_data_clean_common(form.cleaned_data)
        (primers, offset, min_muts, max_muts, which_muts, which_lib, structures, is_single, is_fill_WT, num_mutations) = form_clean_data_3d(form.cleaned_data, sequence)
        is_valid = form_check_valid(3, sequence, primers=primers, min_muts=min_muts, max_muts=max_muts, structures=structures)
        if isinstance(is_valid, HttpResponse):
            return is_valid
        else:
            primers = is_valid[1]

        job_id = random_job_id()
        create_HTML_page_wait(job_id, 3)
        job_entry = Design3D(date=datetime.now(), job_id=job_id, sequence=sequence, structures=simplejson.dumps(structures, sort_keys=True, indent=' ' * 4), tag=tag, status='1', params=simplejson.dumps({'offset': offset, 'min_muts': min_muts, 'max_muts': max_muts, 'which_lib': which_lib, 'num_mutations': num_mutations, 'is_single': is_single, 'is_fill_WT': is_fill_WT}, sort_keys=True, indent=' ' * 4), result=simplejson.dumps({'primer_set': primers}, sort_keys=True, indent=' ' * 4))
        job_entry.save()
        job_list_entry = JobIDs(job_id=job_id, type=3, date=datetime.now())
        job_list_entry.save()
        job = threading.Thread(target=design_3d_wrapper, args=(sequence, structures, primers, tag, offset, which_muts, which_lib, num_mutations, is_single, is_fill_WT, job_id))
        job.start()
        return result_json(job_id)
    else:
        return HttpResponse(simplejson.dumps({'error': '00', 'type': 3}, sort_keys=True, indent=' ' * 4), content_type='application/json')
    return render(request, PATH.HTML_PATH['design_3d'], {'3d_form': form})


def demo_3d(request):
    return HttpResponseRedirect('/result/?job_id=' + ARG['DEMO_3D_ID_1'])

def demo_3d_run(request):
    if 'mode' in request.GET and len(request.GET.get('mode')):
        mode = str(request.GET.get('mode')[0])
    else:
        mode = '1'
    job_id = ARG['DEMO_3D_ID_' + mode]
    create_HTML_page_wait(job_id, 3)
    which_muts = range(ARG['MIN_MUTS'], ARG['MAX_MUTS'] + 1)
    is_single = ARG['IS_SINGLE']
    is_fill_WT = ARG['IS_FILLWT']
    if mode == '2':
        structures = [STR['P4P6_1'], STR['P4P6_2']]
    else:
        structures = [STR['P4P6']]
        is_single = (not is_single)
        is_fill_WT = (not is_fill_WT)

    job = threading.Thread(target=design_3d_wrapper, args=(SEQ['P4P6'], structures, SEQ['PRIMER_SET'], 'P4P6_2HP', ARG['OFFSET'], which_muts, [int(ARG['LIB'])], ARG['NUM_MUT'], is_single, is_fill_WT, job_id))
    job.start()
    return result_json(job_id)


def design_3d_wrapper(sequence, structures, primer_set, tag, offset, which_muts, which_lib, num_mutations, is_single, is_fillWT, job_id):
    try:
        t0 = time.time()
        # time.sleep(15)
        plate = prm_3d.design(sequence, primer_set, structures, offset, num_mutations, which_lib, which_muts, tag, is_single, is_fillWT, True)
        save_result_data(plate, job_id, tag, 3)
        t_total = time.time() - t0
    except Exception:
        t_total = time.time() - t0
        print "\033[41mError(s)\033[0m encountered: \033[94m", sys.exc_info()[0], "\033[0m"
        print traceback.format_exc()
        return create_HTML_page_error(job_id, t_total, 3)

    # when no solution found
    if (not plate.is_success): return create_HTML_page_fail(job_id, 3)

    try:
        mode = 'NORMAL' if len(structures) == 1 else 'DIFF'
        script = HTML_elem_header(job_id, False, 3)
        script += '<div class="alert alert-default" title="Sequence Illustration"><p><span class="glyphicon glyphicon-question-sign"></span>&nbsp;&nbsp;<b>INFO</b>: <b style="color:#ff69bc;">%s</b> <i>Mode</i>; <span>(<span class="glyphicon glyphicon-stats" style="color:#b7bac5;"></span> <u>%d</u>)</span>.<small class="pull-right">(hover on sequence to locate plate coordinates)</small></p><p class="monospace" style="overflow-x:scroll;">__SEQ_ANNOT__</p></div>' % (mode, plate.get('N_CONSTRUCT'))
        script += HTML_elem_time_elapsed(t_total, 3)
        (script, flag) = HTML_comp_plates(plate, script, job_id, 3)
        script += HTML_comp_assembly(plate.echo('assembly'))
        script += HTML_elem_whats_next() + '</p>'
        script = HTML_comp_warnings(flag, script, 3)
        script = HTML_comp_illustration(plate, script, 3)

        job_entry = Design3D.objects.get(job_id=job_id)
        job_entry.status = '2' if job_id not in (ARG['DEMO_3D_ID_1'], ARG['DEMO_3D_ID_2']) else '0'
        job_entry.result = simplejson.dumps({'primer_set': plate.primer_set, 'primers': plate._data['assembly'].primers.tolist()[0:-1], 'tm_overlaps': map(lambda x: round(x, 2), plate._data['assembly'].Tm_overlaps), 'plates': [plate.get('N_PLATE'), plate.get('N_PRIMER')], 'constructs': len(plate._data['constructs']), 'warnings': flag}, sort_keys=True, indent=' ' * 4)
        job_entry.time = t_total
        job_entry.save()
        create_HTML_page_result(script, job_id, 3)
    except Exception:
        print "\033[41mError(s)\033[0m encountered: \033[94m", sys.exc_info()[0], "\033[0m"
        print traceback.format_exc()
        create_HTML_page_error(job_id, t_total, 3)


def design_3d_from_1d(request):
    if 'from' in request.GET:
        referer_job_id = request.GET.get('from')

        form = Design3DForm()
        from_1d = False
        if Design1D.objects.filter(job_id=referer_job_id).exists():
            job_entry = Design1D.objects.get(job_id=referer_job_id)
            primers = ','.join(simplejson.loads(job_entry.result)['primer_set'])
            form = Design3DForm(initial={'sequence': job_entry.sequence, 'tag': job_entry.tag, 'primers': primers})
            from_1d = True
    else:
        return error400(request)
    return design_3d(request, form, from_1d=from_1d)

def design_3d_from_2d(request):
    if 'from' in request.GET:
        referer_job_id = request.GET.get('from')

        form = Design3DForm()
        from_2d = False
        if Design2D.objects.filter(job_id=referer_job_id).exists():
            job_entry = Design2D.objects.get(job_id=referer_job_id)
            params = simplejson.loads(job_entry.params)
            primers = ','.join(simplejson.loads(job_entry.result)['primer_set'])
            form = Design3DForm(initial={'sequence': job_entry.sequence, 'tag': job_entry.tag, 'primers': primers, 'max_muts': params['max_muts'], 'min_muts': params['min_muts'], 'offset': params['offset']})
            from_2d = True
    else:
        return error400(request)
    return design_3d(request, form, from_2d=from_2d)

