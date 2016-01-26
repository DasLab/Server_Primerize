from django.http import HttpResponseRedirect, HttpResponse
#, HttpResponseBadRequest, HttpResponseNotFound, HttpResponseServerError
from django.template import RequestContext
from django.shortcuts import render_to_response

from datetime import datetime
import random
import re
import simplejson
import sys
import threading
import time
import traceback

from src.helper import *
from src.models import *
from src.views import error400

import primerize


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
        tag = re.sub('[^a-zA-Z0-9\ \.\-\_]', '', tag)
        if not tag: tag = 'primer'
        if not min_Tm: min_Tm = ARG['MIN_TM']
        if not max_len: max_len = ARG['MAX_LEN']
        if not min_len: min_len = ARG['MIN_LEN']
        if len(sequence) > 500: min_len = max(30, min_len)
        if (not num_primers) or (not is_num_primers): num_primers = ARG['NUM_PRM']

        msg = ''
        if len(sequence) < 60:
            msg = 'Invalid sequence input (should be <u>at least <b>60</b> nt</u> long and without illegal characters).'
        elif num_primers % 2:
            msg = 'Invalid advanced options input: <b>#</b> number of primers must be <b><u>EVEN</u></b>.'
        if msg:
            return HttpResponse(simplejson.dumps({'error': msg}, sort_keys=True, indent=' ' * 4), content_type='application/json')

        job_id = random_job_id()
        create_wait_html(job_id, 1)
        job_entry = Design1D(date=datetime.now(), job_id=job_id, sequence=sequence, tag=tag, status='1', params=simplejson.dumps({'min_Tm': min_Tm, 'max_len': max_len, 'min_len': min_len, 'num_primers': num_primers, 'is_num_primers': is_num_primers, 'is_check_t7': is_check_t7}, sort_keys=True, indent=' ' * 4))
        job_entry.save()
        job_list_entry = JobIDs(job_id=job_id, type=1, date=datetime.now())
        job_list_entry.save()
        job = threading.Thread(target=design_1d_wrapper, args=(sequence, tag, min_Tm, num_primers, max_len, min_len, is_check_t7, job_id))
        job.start()

        return HttpResponse(simplejson.dumps({'status': 'underway', 'job_id': job_id, 'sequence': sequence, 'tag': tag, 'min_Tm': min_Tm, 'max_len': max_len, 'min_len': min_len, 'num_primers': num_primers, 'is_num_primers': is_num_primers, 'is_check_t7': is_check_t7}, sort_keys=True, indent=' ' * 4), content_type='application/json')
    else:
        return HttpResponse(simplejson.dumps({'error': 'Invalid primary and/or advanced options input.'}, sort_keys=True, indent=' ' * 4), content_type='application/json')
    return render_to_response(PATH.HTML_PATH['design_1d'], {'1d_form': form}, context_instance=RequestContext(request))


def demo_1d(request):
    return HttpResponseRedirect('/result/?job_id=' + ARG['DEMO_1D_ID'])

def demo_1d_run(request):
    job_id = ARG['DEMO_1D_ID']
    create_wait_html(job_id, 1)
    job = threading.Thread(target=design_1d_wrapper, args=(SEQ['P4P6'], 'P4P6_2HP', ARG['MIN_TM'], ARG['NUM_PRM'], ARG['MAX_LEN'], ARG['MIN_LEN'], 1, job_id))
    job.start()
    return HttpResponse(simplejson.dumps({'status': 'underway', 'job_id': job_id, 'sequence': SEQ['P4P6'], 'tag': 'P4P6_2HP', 'min_Tm': ARG['MIN_TM'], 'max_len': ARG['MAX_LEN'], 'min_len': ARG['MIN_LEN'], 'num_primers': ARG['NUM_PRM'], 'is_num_primers': 0, 'is_check_t7': 1}, sort_keys=True, indent=' ' * 4), content_type='application/json')


def random_1d(request):
    sequence = SEQ['T7'] + ''.join(random.choice('CGTA') for _ in xrange(random.randint(100, 500)))
    tag = 'scRNA'
    job_id = random_job_id()
    create_wait_html(job_id, 1)
    job_entry = Design1D(date=datetime.now(), job_id=job_id, sequence=sequence, tag=tag, status='1', params=simplejson.dumps({'min_Tm': ARG['MIN_TM'], 'max_len': ARG['MAX_LEN'], 'min_len': ARG['MIN_LEN'], 'num_primers': ARG['NUM_PRM'], 'is_num_primers': 0, 'is_check_t7': 1}, sort_keys=True, indent=' ' * 4))
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
        if is_t7: (sequence, flag, is_G) = is_t7_present(sequence)
        assembly = prm_1d.design(sequence, min_Tm, num_primers, min_length, max_length, tag)
        t_total = time.time() - t0
    except:
        t_total = time.time() - t0
        print "\033[41mError(s)\033[0m encountered: \033[94m", sys.exc_info()[0], "\033[0m"
        print traceback.format_exc()
        return create_err_html(job_id, t_total, 1)

    # when no solution found
    if (not assembly.is_success):
        html = '<br/><hr/><div class="row"><div class="col-lg-8 col-md-8 col-sm-6 col-xs-6"><h2>Output Result:</h2></div><div class="col-lg-4 col-md-4 col-sm-6 col-xs-6"><h4 class="text-right"><span class="glyphicon glyphicon-search"></span>&nbsp;&nbsp;<span class="label label-violet">JOB_ID</span>: <span class="label label-inverse" id="disp_job_id">%s</span></h4><button class="btn btn-blue pull-right" style="color: #ffffff;" title="Output in plain text" disabled><span class="glyphicon glyphicon-download-alt"></span>&nbsp;&nbsp;Save Result&nbsp;</button></div></div><br/><div class="alert alert-danger"><p><span class="glyphicon glyphicon-minus-sign"></span>&nbsp;&nbsp;<b>FAILURE</b>: No solution found (Primerize run finished without errors).<br/><ul><li>Please examine the advanced options. Possible solutions might be restricted by stringent options combination, especially by minimum Tm and # number of primers. Try again with relaxed the advanced options.</li><li>Certain input sequence, e.g. polyA or large repeats, might be intrinsically difficult for PCR assembly design.</li><li>For further information, please feel free to <a class="btn btn-warning btn-sm" href="/about/#contact" style="color: #ffffff;"><span class="glyphicon glyphicon-send"></span>&nbsp;&nbsp;Contact&nbsp;</a> us to track down the problem.</li></ul></p></div>' % (job_id)
        if job_id != ARG['DEMO_1D_ID']:
            job_entry = Design1D.objects.get(job_id=job_id)
            job_entry.status = '3'
            job_entry.save()
        return create_res_html(html, job_id, 1)
    
    try:
        script = '<br/><hr/><div class="row"><div class="col-lg-8 col-md-8 col-sm-6 col-xs-6"><h2>Output Result:</h2></div><div class="col-lg-4 col-md-4 col-sm-6 col-xs-6"><h4 class="text-right"><span class="glyphicon glyphicon-search"></span>&nbsp;&nbsp;<span class="label label-violet">JOB_ID</span>: <span class="label label-inverse" id="disp_job_id">%s</span></h4><a href="%s" class="btn btn-blue pull-right" style="color: #ffffff;" title="Output in plain text" download><span class="glyphicon glyphicon-download-alt"></span>&nbsp;&nbsp;Save Result&nbsp;</a></div></div><br/><div class="alert alert-warning" title="Mispriming alerts"><p>' % (job_id, '/site_data/1d/result_%s.txt' % job_id)

        warnings = assembly.get('WARNING')
        if len(warnings):
            for i in xrange(len(warnings)):
                w = warnings[i]
                p_1 = '<b>%d</b> %s' % (w[0], primer_suffix_html(w[0] - 1))
                p_2 = ', '.join('<b>%d</b> %s' % (x, primer_suffix_html(x - 1)) for x in w[3])
                script += '<span class="glyphicon glyphicon-exclamation-sign"></span>&nbsp;&nbsp;<b>WARNING</b>: Primer %s can misprime with <span class="label label-default">%d</span>-residue overlap to position <span class="label label-success">%s</span>, which is covered by primers: %s.<br/>' % (p_1, w[1], str(int(w[2])), p_2)
            script += '<span class="glyphicon glyphicon-info-sign"></span>&nbsp;&nbsp;<b>WARNING</b>: One-pot PCR assembly may fail due to mispriming; consider first assembling fragments in a preliminary PCR round (subpool).<br/>'
        else:
            script += '<span class="glyphicon glyphicon-ok-sign"></span>&nbsp;&nbsp;<b>SUCCESS</b>: No potential mis-priming found. See results below.<br/>'
            script = script.replace('alert-warning', 'alert-success')

        script += '</p></div><div class="row"><div class="col-lg-10 col-md-10 col-sm-9 col-xs-9"><div class="alert alert-default" id="col-res-l"><p>__NOTE_T7__</p></div></div><div class="col-lg-2 col-md-2 col-sm-3 col-xs-3"><div class="alert alert-orange text-center" id="col-res-r"> <span class="glyphicon glyphicon-time"></span>&nbsp;&nbsp;<b>Time elapsed</b>:<br/><i>%.1f</i> s.</div></div></div>' % t_total

        script += '<div class="row"><div class="col-lg-12 col-md-12 col-sm-12 col-xs-12"><div class="panel panel-primary"><div class="panel-heading"><h2 class="panel-title"><span class="glyphicon glyphicon-indent-left"></span>&nbsp;&nbsp;Designed Primers</h2></div><div class="panel-body"><table class="table table-striped table-hover" ><thead><tr class="active"><th class="col-lg-1 col-md-1 col-sm-1 col-xs-1">#</th><th class="col-lg-1 col-md-1 col-sm-1 col-xs-1">Length</th><th class="col-lg-10 col-md-10 col-sm-10 col-xs-10">Sequence</th></tr></thead><tbody>'
        for i in xrange(len(assembly.primer_set)):
            script += '<tr><td><b>%d</b> %s</td><td><em>%d</em></td><td style="word-break:break-all" class="monospace">%s</td></tr>' % (i + 1, primer_suffix_html(i), len(assembly.primer_set[i]), assembly.primer_set[i])

        script += '<tr><td colspan="3" style="padding: 0px;"></td></tr></tbody></table></div></div></div></div><div class="row"><div class="col-lg-12 col-md-12 col-sm-12 col-xs-12"><div class="panel panel-green"><div class="panel-heading"><h2 class="panel-title"><span class="glyphicon glyphicon-tasks"></span>&nbsp;&nbsp;Assembly Scheme</h2></div><div class="panel-body"><pre style="font-size:12px;">'

        x = 0
        for line in assembly._data['assembly'].print_lines:
            if line[0] == '~':
                script += '<br/><span class="label-white label-primary">' + line[1] + '</span>'
            elif line[0] == '=':
                script += '<span class="label-warning">' + line[1] + '</span>'
            elif line[0] == '^':
                for char in line[1]:
                    if char in SEQ['valid']:
                        script += '<span class="label-info">' + char + '</span>'
                    else:
                        if char.isdigit():
                            script += '<b>' + char + '</b>'
                        elif char in ('-', '<', '>'):
                            script += '<span class="label-white label-orange">' + char + '</span>'
                        else:
                            script += char
                    script = script.replace('<span class="label-white label-orange">-</span><span class="label-white label-orange">></span>', '<span class="label-white label-orange glyphicon glyphicon-arrow-right" style="margin-left:2px; padding-left:1px;"></span>')
            elif line[0] == "!":
                for char in line[1]:
                    if char in SEQ['valid']:
                        script += '<span class="label-white label-danger">' + char + '</span>'
                    else:
                        if char.isdigit():
                            script += '<b>' + char + '</b>'
                        elif char in ('-', '<', '>'):
                            script += '<span class="label-white label-green">' + char + '</span>'
                        else:
                            script += char
                    script = script.replace('<span class="label-white label-green"><</span><span class="label-white label-green">-</span>', '<span class="label-white label-green glyphicon glyphicon-arrow-left" style="margin-right:2px; padding-right:1px;"></span>')
            elif (line[0] == '$'):
                if line[1].find('xxxx') != -1: 
                    Tm = '%2.1f' % assembly._data['assembly'].Tm_overlaps[x]
                    x += 1
                    script += line[1].replace('x' * len(Tm), '<kbd>%s</kbd>' % Tm)
                elif '|' in line[1]:
                    script += line[1]
            script += '<br/>'

        script += '</pre></div></div></div></div><div class="row"><div class="col-lg-9 col-md-9 col-sm-9 col-xs-9"><p class="lead"><span class="glyphicon glyphicon-question-sign"></span>&nbsp;&nbsp;<b><u><i>What\'s next?</i></u></b> Try our suggested experimental <a class="btn btn-info btn-sm" href="/protocol/#PCR" role="button" style="color: #ffffff;"><span class="glyphicon glyphicon-file"></span>&nbsp;&nbsp;Protocol&nbsp;</a> for PCR assembly. Or go ahead for <code>Mutate-and-Map Plates</code>.</p></div><div class="col-lg-3 col-md-3 col-sm-3 col-xs-3"><a id="btn-1d-to-2d" class="btn btn-primary btn-lg btn-block" href="/design_2d_from_1d/" role="button" style="color: #ffffff;"><span class="glyphicon glyphicon-play-circle"></span>&nbsp;&nbsp;Design&nbsp;</a></div></div><script type="text/javascript">resize();</script>'

        assembly.save(MEDIA_ROOT + '/data/1d/', 'result_%s' % job_id)
        file_name = MEDIA_ROOT + '/data/1d/result_%s.txt' % job_id
        lines = ''.join(open(file_name, 'r').readlines())
        insert_where = '\n\nOUTPUT\n======\n'
        
        if is_t7:
            str_t7 = '<span class="glyphicon glyphicon-plus-sign"></span>&nbsp;&nbsp;T7_CHECK: feature enabled (uncheck the option to disable). T7 promoter sequence '
            if flag:
                str_t7 = str_t7 + 'is present, no action was taken.\n'
            else:
                str_t7 = str_t7 + 'was absent, Primerize automatically prepended it. \n'
            if is_G:
                str_t7 += '<span class="glyphicon glyphicon-ok-sign"></span>&nbsp;&nbsp;SUCCESS: T7 promoter sequence is followed by nucleotides GG.\n'
            else:
                str_t7 += '<span class="glyphicon glyphicon-exclamation-sign"></span>&nbsp;&nbsp;WARNING: T7 promoter sequence is NOT followed by nucleotides GG. Consider modifying the sequence for better transcription.\n'
        else:
            str_t7 = 'T7_CHECK: feature disabled (check the option to enable). No checking was performed.\n'
        lines = lines.replace(insert_where, str_t7.replace('SUCCESS', 'T7_CHECK').replace('WARNING', 'T7_CHECK').replace('<span class="glyphicon glyphicon-ok-sign"></span>&nbsp;&nbsp;', '').replace('<span class="glyphicon glyphicon-plus-sign"></span>&nbsp;&nbsp;', '').replace('<span class="glyphicon glyphicon-exclamation-sign"></span>&nbsp;&nbsp;', '') + insert_where)
        script = script.replace('__NOTE_T7__', str_t7.replace('\n', '<br/>').replace('T7_CHECK', '<b>T7_CHECK</b>').replace('SUCCESS', '<b>SUCCESS</b>').replace('WARNING', '<b>WARNING</b>').replace('NOT', '<u><b>NOT</b></u>').replace('nucleotides GG', 'nucleotides <u>GG</u>'))
        open(file_name, 'w').write(lines)

        if job_id != ARG['DEMO_1D_ID']:
            job_entry = Design1D.objects.get(job_id=job_id)
            job_entry.status = '2'
            job_entry.primers = assembly.primer_set
            job_entry.time = t_total
            job_entry.save()
        create_res_html(script, job_id, 1)
    except:
        print "\033[41mError(s)\033[0m encountered: \033[94m", sys.exc_info()[0], "\033[0m"
        print traceback.format_exc()
        create_err_html(job_id, t_total, 1)


