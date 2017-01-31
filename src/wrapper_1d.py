from django.http import HttpResponseRedirect, HttpResponse
#, HttpResponseBadRequest, HttpResponseNotFound, HttpResponseServerError
from django.shortcuts import render

from datetime import datetime
import random
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


def design_1d(request):
    return render(request, PATH.HTML_PATH['design_1d'], {'1d_form': Design1DForm()})

def design_1d_run(request):
    if request.method != 'POST': return error400(request)
    form = Design1DForm(request.POST)
    if form.is_valid():
        (sequence, tag) = form_data_clean_common(form.cleaned_data)
        (min_Tm, max_len, min_len, num_primers, is_num_primers, is_check_t7) = form_data_clean_1d(form.cleaned_data, sequence)
        if is_check_t7: (sequence, _, _) = is_t7_present(sequence)
        is_valid = form_check_valid_job(1, sequence, num_primers=num_primers)
        if isinstance(is_valid, HttpResponse): return is_valid

        job_id = random_job_id()
        create_HTML_page_wait(job_id, 1)
        job_entry = Design1D(date=datetime.now(), job_id=job_id, sequence=sequence, tag=tag, status='1', params=simplejson.dumps({'min_Tm': min_Tm, 'max_len': max_len, 'min_len': min_len, 'num_primers': num_primers, 'is_num_primers': is_num_primers, 'is_check_t7': is_check_t7}, sort_keys=True, indent=' ' * 4), result=simplejson.dumps({}))
        job_entry.save()
        job_list_entry = JobIDs(job_id=job_id, type=1, date=datetime.now())
        job_list_entry.save()
        job = threading.Thread(target=design_1d_wrapper, args=(sequence, tag, min_Tm, num_primers, max_len, min_len, is_check_t7, job_id))
        job.start()
        return result_json(job_id)
    else:
        return HttpResponse(simplejson.dumps({'error': '00', 'type': 1}, sort_keys=True, indent=' ' * 4), content_type='application/json')
    return render(request, PATH.HTML_PATH['design_1d'], {'1d_form': form})


def demo_1d(request):
    return HttpResponseRedirect('/result/?job_id=' + ARG['DEMO_1D_ID'])

def demo_1d_run(request):
    job_id = ARG['DEMO_1D_ID']
    create_HTML_page_wait(job_id, 1)
    job = threading.Thread(target=design_1d_wrapper, args=(SEQ['P4P6'], 'P4P6_2HP', ARG['MIN_TM'], ARG['NUM_PRM'], ARG['MAX_LEN'], ARG['MIN_LEN'], 1, job_id))
    job.start()
    return result_json(job_id)


def random_1d(request):
    sequence = SEQ['T7'] + ''.join(random.choice('CGTA') for _ in xrange(random.randint(100, 500)))
    tag = 'scRNA'
    job_id = random_job_id()
    create_HTML_page_wait(job_id, 1)
    job_entry = Design1D(date=datetime.now(), job_id=job_id, sequence=sequence, tag=tag, status='1', params=simplejson.dumps({'min_Tm': ARG['MIN_TM'], 'max_len': ARG['MAX_LEN'], 'min_len': ARG['MIN_LEN'], 'num_primers': ARG['NUM_PRM'], 'is_num_primers': 0, 'is_check_t7': 1}, sort_keys=True, indent=' ' * 4), result=simplejson.dumps({}))
    job_entry.save()
    job_list_entry = JobIDs(job_id=job_id, type=1, date=datetime.now())
    job_list_entry.save()
    job = threading.Thread(target=design_1d_wrapper, args=(sequence, tag, ARG['MIN_TM'], ARG['NUM_PRM'], ARG['MAX_LEN'], ARG['MIN_LEN'], 1, job_id))
    job.start()
    return HttpResponseRedirect('/result/?job_id=' + job_id)


def design_1d_wrapper(sequence, tag, min_Tm, num_primers, max_length, min_length, is_t7, job_id):
    try:
        t0 = time.time()
        # time.sleep(15)
        (flag, is_G) = (0, False)
        if is_t7: (sequence, flag, is_G) = is_t7_present(sequence)
        assembly = prm_1d.design(sequence, min_Tm, num_primers, min_length, max_length, tag)
        assembly.save(MEDIA_ROOT + '/data/1d/', 'result_%s' % job_id)
        t_total = time.time() - t0
    except Exception:
        t_total = time.time() - t0
        print "\033[41mError(s)\033[0m encountered: \033[94m", sys.exc_info()[0], "\033[0m"
        print traceback.format_exc()
        return create_HTML_page_error(job_id, t_total, 1)

    # when no solution found
    if (not assembly.is_success): return create_HTML_page_fail(job_id, 1)

    try:
        script = HTML_elem_header(job_id, False, 1)
        script += '<div class="alert alert-warning" title="Mispriming alerts"><p>'
        script = HTML_comp_warnings(assembly, script, [], 1)
        script += '</p></div>' + HTML_elem_time_elapsed(t_total, 1)
        script = HTML_comp_t7_check(job_id, script, flag, is_t7, is_G)
        script += HTML_comp_primers(assembly)
        script += HTML_comp_assembly(assembly.echo('assembly'))
        script += '<div class="row"><div class="col-lg-9 col-md-9 col-sm-9 col-xs-9">%s. Or go ahead for <code>Mutate-and-Map Plates</code> and/or <code>Mutation/Rescue Sets</code>.</p></div><div class="col-lg-3 col-md-3 col-sm-3 col-xs-3"><a id="btn-1d-to-2d" class="btn btn-primary btn-block btn-spa" href="/design_2d_from_1d/" role="button" style="color: #ffffff;"><span class="glyphicon glyphicon-play-circle"></span>&nbsp;&nbsp;Design 2D&nbsp;</a><a id="btn-1d-to-3d" class="btn btn-primary btn-block btn-spa" href="/design_3d_from_1d/" role="button" style="color: #ffffff;"><span class="glyphicon glyphicon-play-circle"></span>&nbsp;&nbsp;Design 3D&nbsp;</a></div></div>' % HTML_elem_whats_next()

        job_entry = Design1D.objects.get(job_id=job_id)
        job_entry.status = '2' if job_id != ARG['DEMO_1D_ID'] else '0'
        job_entry.result = simplejson.dumps({'primer_set': assembly.primer_set, 'primers': assembly._data['assembly'].primers.tolist()[0:-1], 'tm_overlaps': map(lambda x: round(x, 2), assembly._data['assembly'].Tm_overlaps), 'warnings': assembly._data['warnings']}, sort_keys=True, indent=' ' * 4)
        job_entry.time = t_total
        job_entry.save()

        create_HTML_page_result(script, job_id, 1)
    except Exception:
        print "\033[41mError(s)\033[0m encountered: \033[94m", sys.exc_info()[0], "\033[0m"
        print traceback.format_exc()
        create_HTML_page_error(job_id, t_total, 1)


