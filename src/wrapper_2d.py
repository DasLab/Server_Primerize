from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest, HttpResponseNotFound, HttpResponseServerError
from django.template import RequestContext
from django.shortcuts import render, render_to_response

from datetime import datetime
import random
import re
import simplejson
import subprocess
import threading
import time
import traceback

from src.helper import *
from src.models import *
from src.pymerize.primerize_2d import *


def design_2d(request):
    return render_to_response(PATH.HTML_PATH['design_2d'], {'2d_form': Design2DForm()}, context_instance=RequestContext(request))

def design_2d_run(request):
    if request.method != 'POST': return HttpResponseBadRequest('Invalid request.')
    form = Design2DForm(request.POST)
    if form.is_valid():
        sequence = form.cleaned_data['sequence']
        tag = form.cleaned_data['tag']
        primers = form.cleaned_data['primers']
        offset = form.cleaned_data['offset']
        min_muts = form.cleaned_data['min_muts']
        max_muts = form.cleaned_data['max_muts']
        lib = form.cleaned_data['lib']

        sequence = re.sub('[^' + ''.join(SEQ['valid']) + ']', '', sequence.upper().replace('U', 'T'))
        tag = re.sub('[^a-zA-Z0-9\ \.\-\_]', '', tag)
        primers = re.sub('[^ACGTUacgtu\ \,]', '', primers)
        primers = [str(p.strip()) for p in primers.split(',') if p.strip()]
        if not primers:
            primers = Primer_Assembly(sequence).primer_set
        if not tag: tag = 'primer'
        if not offset: offset = 0
        if not min_muts: min_muts = 1 - offset
        if not max_muts: max_muts = len(sequence) + 1 - offset
        if not lib: lib = '1'
        which_lib = [int(lib)]
        which_muts = range(min_muts, max_muts + 1)

        msg = ''
        if len(sequence) < 60:
            msg = 'Invalid sequence input (should be <u>at least <b>60</b> nt</u> long and without illegal characters).'
        elif len(primers) % 2:
            msg = 'Invalid primers input (should be in <b>pairs</b>).'
        elif min_muts > max_muts:
            msg = 'Invalid mutation starting and ending positions: <b>starting</b> should be <u>lower or equal</u> than <b>ending</b>.'
        if msg:
            return HttpResponse(simplejson.dumps({'error': msg}), content_type='application/json')

        job_id = random_job_id()
        create_wait_html(job_id, 2)
        job_entry = Design2D(date=datetime.now(), job_id=job_id, sequence=sequence, primers=primers, tag=tag, status='1', params=simplejson.dumps({'offset': offset, 'min_muts': min_muts, 'max_muts': max_muts, 'which_lib': which_lib}))
        job_entry.save()
        job_list_entry = JobIDs(job_id=job_id, type=2, date=datetime.now())
        job_list_entry.save()
        job = threading.Thread(target=design_2d_wrapper, args=(sequence, primers, tag, offset, which_muts, which_lib, job_id))
        job.start()

        return HttpResponse(simplejson.dumps({'status': 'underway', 'job_id': job_id, 'sequence': sequence, 'tag': tag, 'primers': primers, 'min_muts': min_muts, 'max_muts': max_muts, 'offset': offset, 'lib': lib}), content_type='application/json')
    else:
        return HttpResponse(simplejson.dumps({'error': 'Invalid primary and/or advanced options input.'}), content_type='application/json')
    return render_to_response(PATH.HTML_PATH['design_2d'], {'2d_form': form}, context_instance=RequestContext(request))


def demo_2d(request):
    return HttpResponseRedirect('/result/?job_id=' + ARG['DEMO_2D_ID'])

def demo_2d_run(request):
    job_id = ARG['DEMO_2D_ID']
    create_wait_html(job_id, 2)
    which_muts = range(ARG['MIN_MUTS'], ARG['MAX_MUTS'] + 1)
    job = threading.Thread(target=design_2d_wrapper, args=(SEQ['P4P6'], SEQ['PRIMER_SET'], 'P4P6_2HP', ARG['OFFSET'], which_muts, [int(ARG['LIB'])], job_id))
    job.start()
    return HttpResponse(simplejson.dumps({'status': 'underway', 'job_id': job_id, 'sequence': SEQ['P4P6'], 'tag': 'P4P6_2HP', 'primers': SEQ['PRIMER_SET'], 'min_muts': ARG['MIN_MUTS'], 'max_muts': ARG['MAX_MUTS'], 'offset': ARG['OFFSET'], 'lib': ARG['LIB']}), content_type='application/json')


def random_2d(request):
    # sequence = SEQ['T7'] + ''.join(random.choice('CGTA') for _ in xrange(random.randint(100, 500)))
    # tag = 'scRNA'
    # job_id = random_job_id()
    # create_wait_html(job_id, 2)
    # job_entry = Design2D(date=datetime.now(), job_id=job_id, sequence=sequence, tag=tag, status='1', params=simplejson.dumps({'min_Tm': ARG['MIN_TM'], 'max_len': ARG['MAX_LEN'], 'min_len': ARG['MIN_LEN'], 'num_primers': ARG['NUM_PRM'], 'is_num_primers': 0, 'is_check_t7': 1}))
    # job_entry.save()
    # job_list_entry = JobIDs(job_id=job_id, type=1, date=datetime.now())
    # job_list_entry.save()
    # job = threading.Thread(target=design_2d_wrapper, args=(sequence, tag, ARG['MIN_TM'], ARG['NUM_PRM'], ARG['MAX_LEN'], ARG['MIN_LEN'], 1, job_id))
    # job.start()
    # return HttpResponseRedirect('/result/?job_id=' + job_id)
    pass


def design_2d_wrapper(sequence, primer_set, tag, offset, which_muts, which_lib, job_id):
    try:
        t0 = time.time()
        # time.sleep(5)
        plate = Mutate_Map(sequence, primer_set, offset, which_muts, which_lib, tag)
        if not plate.is_error:
            dir_name = os.path.join(MEDIA_ROOT, 'data/2d/result_%s' % job_id)
            if not os.path.exists(dir_name):
                os.mkdir(dir_name)
            plate.output_constructs(dir_name)
            plate.output_spreadsheet(dir_name)
            subprocess.check_call('cd %s && zip -rm result_%s.zip result_%s' % (os.path.join(MEDIA_ROOT, 'data/2d/'), job_id, job_id), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        t_total = time.time() - t0
    except:
        t_total = time.time() - t0
        print "\033[41mError(s)\033[0m encountered: \033[94m", sys.exc_info()[0], "\033[0m"
        print traceback.format_exc()
        return create_err_html(job_id, t_total, 2)

    # when no solution found
    if (plate.is_error):
        html = '<br/><hr/><div class="row"><div class="col-md-8"><h2>Output Result:</h2></div><div class="col-md-4"><h4 class="text-right"><span class="glyphicon glyphicon-search"></span>&nbsp;&nbsp;<span class="label label-violet">JOB_ID</span>: <span class="label label-inverse">%s</span></h4><a href="%s" class="btn btn-blue pull-right" style="color: #ffffff;" title="Output in plain text" download disabled>&nbsp;Save Result&nbsp;</a></div></div><br/><div class="alert alert-danger"><p><span class="glyphicon glyphicon-minus-sign"></span>&nbsp;&nbsp;<b>FAILURE</b>: No solution found (Primerize run finished without errors).<br/><ul><li>Please examine the advanced options. Possible solutions might be restricted by stringent options combination, especially by minimum Tm and # number of primers. Try again with relaxed the advanced options.</li><li>Certain input sequence, e.g. polyA or large repeats, might be intrinsically difficult for PCR assembly design.</li><li>For further information, please feel free to <a class="btn btn-warning btn-sm" href="/about/#contact" style="color: #ffffff;">Contact</a> us to track down the problem.</li></ul></p>' % (job_id, '/site_data/2d/result_%s.txt' % job_id)
        if job_id != ARG['DEMO_2D_ID']:
            job_entry = Design2D.objects.get(job_id=job_id)
            job_entry.status = '3'
            job_entry.save()
        return create_res_html(html, job_id, 2)
    
    try:
        script = '<br/><hr/><div class="row"><div class="col-md-8"><h2>Output Result:</h2></div><div class="col-md-4"><h4 class="text-right"><span class="glyphicon glyphicon-search"></span>&nbsp;&nbsp;<span class="label label-violet">JOB_ID</span>: <span class="label label-inverse">%s</span></h4><a href="%s" class="btn btn-blue pull-right" style="color: #ffffff;" title="Output in plain text" download>&nbsp;Save Result&nbsp;</a></div></div><br/>' % (job_id, '/site_data/2d/result_%s.zip' % job_id)
        script += '<div class="row"><div class="col-md-10"><div class="alert alert-default"><p>__NOTE_T7__</p></div></div><div class="col-md-2"><div class="alert alert-orange text-center"> <span class="glyphicon glyphicon-time"></span>&nbsp;&nbsp;<b>Time elapsed</b>:<br/><i>%.1f</i> s.</div></div></div>' % t_total

        script += '<div class="row"><div class="col-md-12"><div class="panel panel-green"><div class="panel-heading"><h2 class="panel-title"><span class="glyphicon glyphicon-tasks"></span>&nbsp;&nbsp;Assembly Scheme</h2></div><div class="panel-body"><pre style="font-size:12px;">'

        (_, _, print_lines, Tm_overlaps) = draw_assembly(plate.sequence, plate.primers, plate.name)
        x = 0
        for line in print_lines:
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
                    Tm = '%2.1f' % Tm_overlaps[x]
                    x += 1
                    script += line[1].replace('x' * len(Tm), '<kbd>%s</kbd>' % Tm)
                elif '|' in line[1]:
                    script += line[1]
            script += '<br/>'
        script += '</pre></div></div></div></div><div class="row"><div class="col-md-12"><div class="panel panel-primary"><div class="panel-heading"><h2 class="panel-title"><span class="glyphicon glyphicon-th"></span>&nbsp;&nbsp;Plate Layout</h2></div><div class="panel-body">'

        json = {'plates': {}}
        for i in xrange(plate.N_plates):
            json['plates'][i + 1] = {'primers': {}}
            script += '<div class="row"><div class="col-md-12"><p class="lead">Plate # <span class="label label-orange">%d</span></p></div></div><div class="row">' % (i + 1)

            for j in xrange(plate.N_primers):
                primer_sequences = plate.plates[j][i]
                num_primers_on_plate = primer_sequences.get_count()

                if num_primers_on_plate:
                    json['plates'][i + 1]['primers'][j + 1] = []
                    script += '<div class="col-md-3"><div class="thumbnail"><div id="svg_plt_%d_prm_%d"></div><div class="caption"><p class="text-center center-block" style="margin-bottom:0px;"><i>Primer</i> <b>%d</b> %s</p></div></div></div>' % (i + 1, j + 1, j + 1, primer_suffix_html(j))

                    for k in xrange(96):
                        if primer_sequences.data.has_key(k + 1):
                            row = primer_sequences.data[k + 1]
                            json['plates'][i + 1]['primers'][j + 1].append({'coord': k + 1, 'label': row[0], 'pos': num_to_coord(k + 1), 'sequence': row[1]})
                        else:
                            json['plates'][i + 1]['primers'][j + 1].append({'coord': k + 1})


            script += '</div>'

        open(os.path.join(MEDIA_ROOT, 'data/2d/result_%s.json' % job_id), 'w').write(simplejson.dumps(json))
        script += '</div></div></div></div></div><p class="lead"><span class="glyphicon glyphicon-question-sign"></span>&nbsp;&nbsp;<b><u><i>What next?</i></u></b> Try our suggested experimental <a class="btn btn-info btn-sm" href="/protocol/" role="button" style="color: #ffffff;">&nbsp;&nbsp;Protocol&nbsp;&nbsp;</a> for PCR assembly.</p>'
        # script += plate.print_constructs().replace('\033[96m', '<span class="label label-info">').replace('\033[93m', '<span class="label label-success">').replace('\033[91m', '<span class="label label-danger">').replace('\033[94m', '<span class="label label-primary">').replace('\033[41m', '<span class="label label-magenta">').replace('\033[100m', '<span class="label label-default">').replace('\033[95m', '<span class="label label-violet">').replace('\033[92m', '<span class="label label-orange">').replace('\033[0m', '</span>').replace('\n', '<br/>')

        if job_id != ARG['DEMO_2D_ID']:
            job_entry = Design2D.objects.get(job_id=job_id)
            job_entry.status = '2'
            # job_entry.plates = assembly.primer_set
            job_entry.time = t_total
            job_entry.save()
        create_res_html(script, job_id, 2)
    except:
        print "\033[41mError(s)\033[0m encountered: \033[94m", sys.exc_info()[0], "\033[0m"
        print traceback.format_exc()
        create_err_html(job_id, t_total, 2)


