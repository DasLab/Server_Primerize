from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest, HttpResponseNotFound, HttpResponseServerError
from django.template import RequestContext
from django.shortcuts import render, render_to_response

from datetime import datetime
import random
import re
import simplejson
import threading
import time
import traceback

from src.helper import *
from src.models import *
from src.pymerize.primerize import *


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
        job_entry = Design1D(date=datetime.now(), job_id=job_id, sequence=sequence, tag=tag, status='1', params=simplejson.dumps({'min_Tm': min_Tm, 'max_len': max_len, 'min_len': min_len, 'num_primers': num_primers, 'is_num_primers': is_num_primers, 'is_check_t7': is_check_t7}))
        job_entry.save()
        job_list_entry = JobIDs(job_id=job_id, type=1, date=datetime.now())
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


def random_1d(request):
    sequence = SEQ['T7'] + ''.join(random.choice('CGTA') for _ in xrange(random.randint(100, 500)))
    tag = 'scRNA'
    job_id = random_job_id()
    create_wait_html(job_id)
    job_entry = Design1D(date=datetime.now(), job_id=job_id, sequence=sequence, tag=tag, status='1', params=simplejson.dumps({'min_Tm': ARG['MIN_TM'], 'max_len': ARG['MAX_LEN'], 'min_len': ARG['MIN_LEN'], 'num_primers': ARG['NUM_PRM'], 'is_num_primers': 0, 'is_check_t7': 1}))
    job_entry.save()
    job_list_entry = JobIDs(job_id=job_id, type=1, date=datetime.now())
    job_list_entry.save()
    job = threading.Thread(target=design_1d_wrapper, args=(sequence, tag, ARG['MIN_TM'], ARG['NUM_PRM'], ARG['MAX_LEN'], ARG['MIN_LEN'], 1, job_id))
    job.start()
    return HttpResponseRedirect('/result/?job_id=' + job_id)


def design_1d_wrapper(sequence, tag, min_Tm, num_primers, max_length, min_length, is_t7, job_id):
    try:
        t0 = time.time()
        # time.sleep(5)
        if is_t7: (sequence, flag, is_G) = is_t7_present(sequence)
        assembly = Primer_Assembly(sequence, min_Tm, num_primers, min_length, max_length, tag)
        t_total = time.time() - t0
    except:
        t_total = time.time() - t0
        print "\033[41mError(s)\033[0m encountered: \033[94m", sys.exc_info()[0], "\033[0m"
        print traceback.format_exc()
        return create_err_html(job_id, t_total)

    # when no solution found
    if (not assembly.is_solution):
        html = '<br/><hr/><div class="container theme-showcase"><div class="row"><div class="col-md-8"><h2>Output Result:</h2></div><div class="col-md-4"><h4 class="text-right"><span class="glyphicon glyphicon-search"></span>&nbsp;&nbsp;<span class="label label-violet">JOB_ID</span>: <span class="label label-inverse">%s</span></h4><a href="%s" class="btn btn-blue pull-right" style="color: #ffffff;" title="Output in plain text" download disabled>&nbsp;Save Result&nbsp;</a></div></div><br/><div class="alert alert-danger"><p><span class="glyphicon glyphicon-minus-sign"></span>&nbsp;&nbsp;<b>FAILURE</b>: No solution found (Primerize run finished without errors).<br/><ul><li>Please examine the advanced options. Possible solutions might be restricted by stringent options combination, especially by minimum Tm and # number of primers. Try again with relaxed the advanced options.</li><li>Certain input sequence, e.g. polyA or large repeats, might be intrinsically difficult for PCR assembly design.</li><li>For further information, please feel free to <a class="btn btn-warning btn-sm" href="/about/#contact" style="color: #ffffff;">Contact</a> us to track down the problem.</li></ul></p></div>' % (job_id, '/site_data/1d/result_%s.txt' % job_id)
        if job_id != ARG['DEMO_1D_ID']:
            job_entry = Design1D.objects.get(job_id=job_id)
            job_entry.status = '3'
            job_entry.save()
        return create_res_html(html, job_id)
    
    try:
        script = ''
        if len(assembly.warnings):
            script += '<br/><hr/><div class="container theme-showcase"><div class="row"><div class="col-md-8"><h2>Output Result:</h2></div><div class="col-md-4"><h4 class="text-right"><span class="glyphicon glyphicon-search"></span>&nbsp;&nbsp;<span class="label label-violet">JOB_ID</span>: <span class="label label-inverse">%s</span></h4><a href="%s" class="btn btn-blue pull-right" style="color: #ffffff;" title="Output in plain text" download>&nbsp;Save Result&nbsp;</a></div></div><br/><div class="alert alert-warning" title="Mispriming alerts"><p>' % (job_id, '/site_data/1d/result_%s.txt' % job_id)
            for i in xrange(len(assembly.warnings)):
                warning = assembly.warnings[i]
                p_1 = '<b>%d</b>%s' % (warning[0], primer_suffix_html(warning[0] - 1))
                p_2 = ', '.join('<b>%d</b>%s' % (x, primer_suffix_html(x - 1)) for x in warning[3])
                script += '<span class="glyphicon glyphicon-exclamation-sign"></span>&nbsp;&nbsp;<b>WARNING</b>: Primer %s can misprime with <span class="label label-default">%d</span>-residue overlap to position <span class="label label-success">%s</span>, which is covered by primers: %s.<br/>' % (p_1, warning[1], str(int(warning[2])), p_2)
            script += '<span class="glyphicon glyphicon-info-sign"></span>&nbsp;&nbsp;<b>WARNING</b>: One-pot PCR assembly may fail due to mispriming; consider first assembling fragments in a preliminary PCR round (subpool).<br/>'
        else:
            script += '<div class="container theme-showcase"><div class="row"><div class="col-md-8"><h2>Output Result:</h2></div><div class="col-md-4"><h4 class="text-right"><span class="label label-violet">JOB_ID</span>: <span class="label label-inverse">%s</span></h4><a href="%s" class="btn btn-blue pull-right" title="Output in plain text" download>&nbsp;Download&nbsp;</a></div></div><br/><div class="alert alert-success" title="No alerts"><p>' % (job_id, '/site_data/1d/result_%s.txt' % job_id)
            script += '<span class="glyphicon glyphicon-ok-sign"></span>&nbsp;&nbsp;<b>SUCCESS</b>: No potential mis-priming found. See results below.<br/>'

        script += '</p></div><div class="row"><div class="col-md-10"><div class="alert alert-default"><p>__NOTE_T7__</p></div></div><div class="col-md-2"><div class="alert alert-orange text-center"> <span class="glyphicon glyphicon-time"></span>&nbsp;&nbsp;<b>Time elapsed</b>:<br/><i>%.1f</i> s.</div></div></div>' % t_total

        script += '<div class="row"><div class="col-md-12"><div class="panel panel-primary"><div class="panel-heading"><h2 class="panel-title"><span class="glyphicon glyphicon-indent-left"></span>&nbsp;&nbsp;Designed Primers</h2></div><div class="panel-body"><table class="table table-striped table-hover" ><thead><tr><th class="col-md-1">#</th><th class="col-md-1">Length</th><th class="col-md-10">Sequence</th></tr></thead><tbody>'
        for i in xrange(len(assembly.primer_set)):
            script += '<tr><td><b>%d%s</b></td><td><em>%d</td><td style="word-break: break-all;">%s</td></tr>' % (i + 1, primer_suffix_html(i), len(assembly.primer_set[i]), assembly.primer_set[i])

        script += '</tbody></table></div></div></div></div><div class="row"><div class="col-md-12"><div class="panel panel-green"><div class="panel-heading"><h2 class="panel-title"><span class="glyphicon glyphicon-tasks"></span>&nbsp;&nbsp;Assembly Scheme</h2></div><div class="panel-body"><pre>'

        x = 0
        for line in assembly.print_lines:
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
                    script = script.replace('<span class="label-white label-orange">-</span><span class="label-white label-orange">></span>', '<span class="label-white label-orange glyphicon glyphicon-circle-arrow-right"></span>')
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
                    script = script.replace('<span class="label-white label-green"><</span><span class="label-white label-green">-</span>', '<span class="label-white label-green glyphicon glyphicon-circle-arrow-left"></span>')
            elif (line[0] == '$'):
                if line[1].find('xxxx') != -1: 
                    Tm = '%2.1f' % assembly.Tm_overlaps[x]
                    x += 1
                    script += line[1].replace('x' * len(Tm), '<kbd>%s</kbd>' % Tm)
                elif '|' in line[1]:
                    script += line[1]
            script += '<br/>'

        script += '</pre></div></div></div></div><p class="lead"><span class="glyphicon glyphicon-question-sign"></span>&nbsp;&nbsp;<b><u><i>What next?</i></u></b> Try our suggested experimental <a class="btn btn-info btn-sm" href="/protocol/" role="button" style="color: #ffffff;">&nbsp;&nbsp;Protocol&nbsp;&nbsp;</a> for PCR assembly.</p> </div>'

        file_name = MEDIA_ROOT + '/data/1d/result_%s.txt' % job_id
        f = open(file_name, 'w')

        f.write('Primerize Result\n\nINPUT\n=====\n%s\n' % sequence)
        f.write('#\nMIN_TM: %.1f\n' % min_Tm)
        if num_primers == ARG['NUM_PRM']:
            f.write('NUM_PRIMERS: auto (unspecified)')
        else:
            f.write('NUM_PRIMERS: %d' % num_primers)
        f.write('\nMAX_LENGTH: %d\nMIN_LENGTH: %d\n' % (max_length, min_length))
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
        f.write(str_t7.replace('SUCCESS', 'T7_CHECK').replace('WARNING', 'T7_CHECK').replace('<span class="glyphicon glyphicon-ok-sign"></span>&nbsp;&nbsp;', '').replace('<span class="glyphicon glyphicon-plus-sign"></span>&nbsp;&nbsp;', '').replace('<span class="glyphicon glyphicon-exclamation-sign"></span>&nbsp;&nbsp;', ''))
        script = script.replace('__NOTE_T7__', str_t7.replace('\n', '<br/>').replace('T7_CHECK', '<b>T7_CHECK</b>').replace('SUCCESS', '<b>SUCCESS</b>').replace('WARNING', '<b>WARNING</b>').replace('NOT', '<u><b>NOT</b></u>').replace('nucleotides GG', 'nucleotides <u>GG</u>'))

        f.write('\n\nOUTPUT\n======\n')
        lines = assembly.print_assembly() + assembly.print_primers() + assembly.print_warnings()
        lines = lines.replace('\033[0m', '').replace('\033[100m', '').replace('\033[92m', '').replace('\033[93m', '').replace('\033[94m', '').replace('\033[95m', '').replace('\033[96m', '').replace('\033[41m', '')
        f.write(lines)
        f.write('#\n\n------/* IDT USER: for primer ordering, copy and paste to Bulk Input */------\n------/* START */------\n')
        for i in xrange(len(assembly.primer_set)):
            if i % 2:
                suffix = 'R'
            else:
                suffix = 'F'
            f.write('%s-%d%s\t%s\t\t25nm\tSTD\n' % (tag, i + 1, suffix, assembly.primer_set[i]))
        f.write('------/* END */------\n------/* NOTE: use "Lab Ready" for "Normalization" */------\n')
        f.close()

        if job_id != ARG['DEMO_1D_ID']:
            job_entry = Design1D.objects.get(job_id=job_id)
            job_entry.status = '2'
            job_entry.primers = assembly.primer_set
            job_entry.time = t_total
            job_entry.save()
        create_res_html(script, job_id)
    except:
        print "\033[41mError(s)\033[0m encountered: \033[94m", sys.exc_info()[0], "\033[0m"
        print traceback.format_exc()
        create_err_html(job_id, t_total)


