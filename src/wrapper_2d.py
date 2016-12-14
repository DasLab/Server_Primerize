from django.http import HttpResponseRedirect, HttpResponse
#, HttpResponseBadRequest, HttpResponseNotFound, HttpResponseServerError
from django.shortcuts import render

from datetime import datetime
import random
import simplejson
# import subprocess
import sys
import threading
import time
import traceback

from src.helper import *
from src.models import *
from src.views import result_json, error400


def design_2d(request, form=Design2DForm(), from_1d=False):
    return render(request, PATH.HTML_PATH['design_2d'], {'2d_form': form, 'from_1d': from_1d})

def design_2d_run(request):
    if request.method != 'POST': return error400(request)
    form = Design2DForm(request.POST)
    if form.is_valid():
        (sequence, tag) = form_data_clean_common(form.cleaned_data)
        (primers, offset, min_muts, max_muts, which_muts, which_lib) = form_clean_data_2d(form.cleaned_data, sequence)
        is_valid = form_check_valid(2, sequence, primers=primers, min_muts=min_muts, max_muts=max_muts)
        if isinstance(is_valid, HttpResponse):
            return is_valid
        else:
            primers = is_valid[1]

        job_id = random_job_id()
        create_wait_html(job_id, 2)
        job_entry = Design2D(date=datetime.now(), job_id=job_id, sequence=sequence, tag=tag, status='1', params=simplejson.dumps({'offset': offset, 'min_muts': min_muts, 'max_muts': max_muts, 'which_lib': which_lib}, sort_keys=True, indent=' ' * 4), result=simplejson.dumps({'primer_set': primers}, sort_keys=True, indent=' ' * 4))
        job_entry.save()
        job_list_entry = JobIDs(job_id=job_id, type=2, date=datetime.now())
        job_list_entry.save()
        job = threading.Thread(target=design_2d_wrapper, args=(sequence, primers, tag, offset, which_muts, which_lib, job_id))
        job.start()
        return result_json(job_id)
    else:
        return HttpResponse(simplejson.dumps({'error': '00', 'type': 2}, sort_keys=True, indent=' ' * 4), content_type='application/json')
    return render(request, PATH.HTML_PATH['design_2d'], {'2d_form': form})


def demo_2d(request):
    return HttpResponseRedirect('/result/?job_id=' + ARG['DEMO_2D_ID'])

def demo_2d_run(request):
    job_id = ARG['DEMO_2D_ID']
    create_wait_html(job_id, 2)
    which_muts = range(ARG['MIN_MUTS'], ARG['MAX_MUTS'] + 1)
    job = threading.Thread(target=design_2d_wrapper, args=(SEQ['P4P6'], SEQ['PRIMER_SET'], 'P4P6_2HP', ARG['OFFSET'], which_muts, [int(ARG['LIB'])], job_id))
    job.start()
    return result_json(job_id)


def random_2d(request):
    sequence = SEQ['T7'] + ''.join(random.choice('CGTA') for _ in xrange(random.randint(100, 500)))
    assembly = prm_1d.design(sequence)
    if assembly.is_success:
        primers = assembly.primer_set
    else:
        primers = ''
    tag = 'scRNA'
    offset = 0
    (which_muts, min_muts, max_muts) = primerize.util.get_mut_range(None, None, offset, sequence)
    lib = '1'
    which_lib = [int(lib)]

    job_id = random_job_id()
    create_wait_html(job_id, 2)
    job_entry = Design2D(date=datetime.now(), job_id=job_id, sequence=sequence, tag=tag, status='1', params=simplejson.dumps({'offset': offset, 'min_muts': min_muts, 'max_muts': max_muts, 'which_lib': which_lib}, sort_keys=True, indent=' ' * 4), result=simplejson.dumps({'primer_set': primers}, sort_keys=True, indent=' ' * 4))
    job_entry.save()
    job_list_entry = JobIDs(job_id=job_id, type=2, date=datetime.now())
    job_list_entry.save()
    job = threading.Thread(target=design_2d_wrapper, args=(sequence, primers, tag, offset, which_muts, which_lib, job_id))
    job.start()
    return HttpResponseRedirect('/result/?job_id=' + job_id)


def design_2d_wrapper(sequence, primer_set, tag, offset, which_muts, which_lib, job_id):
    try:
        t0 = time.time()
        # time.sleep(15)
        plate = prm_2d.design(sequence, primer_set, offset, which_muts, which_lib, tag, True)
        save_result_data(plate, job_id, tag, 2)
        t_total = time.time() - t0
    except Exception:
        t_total = time.time() - t0
        print "\033[41mError(s)\033[0m encountered: \033[94m", sys.exc_info()[0], "\033[0m"
        print traceback.format_exc()
        return create_err_html(job_id, t_total, 2)

    # when no solution found
    if (not plate.is_success): return create_HTML_no_solution(job_id, 2)

    try:
        script = output_header_html(job_id, 2)
        script += '<div class="alert alert-default" title="Sequence Illustration"><p><span class="glyphicon glyphicon-question-sign"></span>&nbsp;&nbsp;<b>INFO</b>: <span>(<span class="glyphicon glyphicon-stats" style="color:#b7bac5;"></span> <u>%d</u>)</span><span class="monospace pull-right">__SEQ_ANNOT__</span></p></div>' % plate.get('N_CONSTRUCT')
        script += time_elapsed_html(t_total, 2)
        (script, flag) = create_HTML_plates(plate, script, job_id, 2)
        script += create_HTML_assembly(plate.echo('assembly'))
        script += '<div class="row"><div class="col-lg-9 col-md-9 col-sm-9 col-xs-9">%s. Or go ahead for <code>Mutation/Rescue Sets</code>.</p></div><div class="col-lg-3 col-md-3 col-sm-3 col-xs-3"><a id="btn-2d-to-3d" class="btn btn-primary btn-block btn-spa" href="/design_3d_from_2d/" role="button" style="color: #ffffff;"><span class="glyphicon glyphicon-play-circle"></span>&nbsp;&nbsp;Design 3D&nbsp;</a></div></div>' % whats_next_html()
        script = create_HTML_warnings(flag, script, 2)
        script = create_HTML_illustration(plate, script, 2)

        job_entry = Design2D.objects.get(job_id=job_id)
        job_entry.status = '2' if job_id != ARG['DEMO_2D_ID'] else '0'
        job_entry.result = simplejson.dumps({'primer_set': plate.primer_set, 'primers': plate._data['assembly'].primers.tolist()[0:-1], 'tm_overlaps': map(lambda x: round(x, 2), plate._data['assembly'].Tm_overlaps), 'plates': [plate.get('N_PLATE'), plate.get('N_PRIMER')], 'constructs': len(plate._data['constructs']), 'warnings': flag}, sort_keys=True, indent=' ' * 4)
        job_entry.time = t_total
        job_entry.save()
        create_res_html(script, job_id, 2)
    except Exception:
        print "\033[41mError(s)\033[0m encountered: \033[94m", sys.exc_info()[0], "\033[0m"
        print traceback.format_exc()
        create_err_html(job_id, t_total, 2)


def design_2d_from_1d(request):
    if 'from' in request.GET:
        referer_job_id = request.GET.get('from')

        form = Design2DForm()
        from_1d = False
        if Design1D.objects.filter(job_id=referer_job_id).exists():
            job_entry = Design1D.objects.get(job_id=referer_job_id)
            primers = ','.join(simplejson.loads(job_entry.result)['primer_set'])
            form = Design2DForm(initial={'sequence': job_entry.sequence, 'tag': job_entry.tag, 'primers': primers})
            from_1d = True
    else:
        return error400(request)

    return design_2d(request, form, from_1d)

