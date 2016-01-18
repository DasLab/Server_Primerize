from django.http import HttpResponseRedirect, HttpResponse
#, HttpResponseBadRequest, HttpResponseNotFound, HttpResponseServerError
from django.template import RequestContext
from django.shortcuts import render_to_response

from datetime import datetime
import glob
import os
import random
import re
import simplejson
import shutil
# import subprocess
import sys
import threading
import time
import traceback
import zipfile

from src.helper import *
from src.models import *

import primerize



def design_2d(request, form=Design2DForm(), from_1d=False):
    return render_to_response(PATH.HTML_PATH['design_2d'], {'2d_form': form, 'from_1d': from_1d}, context_instance=RequestContext(request))

def design_2d_run(request):
    if request.method != 'POST': return error400(request)
    form = Design2DForm(request.POST)
    msg = ''
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
            assembly = prm_1d.design(sequence)
            if assembly.is_success:
                primers = assembly.primer_set
            else:
                msg = '<b>No assembly solution</b> found for sequence input under default constraints. Please supply a working assembly scheme (primers).'
        if not tag: tag = 'primer'
        if not offset: offset = 0
        (which_muts, min_muts, max_muts) = primerize.util.get_mut_range(min_muts, max_muts, offset, sequence)
        if not lib: lib = '1'
        which_lib = [int(lib)]

        if len(sequence) < 60:
            msg = 'Invalid sequence input (should be <u>at least <b>60</b> nt</u> long and without illegal characters).'
        elif len(primers) % 2:
            msg = 'Invalid primers input (should be in <b>pairs</b>).'
        elif min_muts > max_muts:
            msg = 'Invalid mutation starting and ending positions: <b>starting</b> should be <u>lower than</u> or <u>equal to</u> <b>ending</b>.'
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
    job_entry = Design2D(date=datetime.now(), job_id=job_id, sequence=sequence, primers=primers, tag=tag, status='1', params=simplejson.dumps({'offset': offset, 'min_muts': min_muts, 'max_muts': max_muts, 'which_lib': which_lib}))
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
        plate = prm_2d.design(sequence, primer_set, offset, which_muts, which_lib, tag)
        if plate.is_success:
            dir_name = os.path.join(MEDIA_ROOT, 'data/2d/result_%s' % job_id)
            if not os.path.exists(dir_name): os.mkdir(dir_name)
            plate.save('', path=dir_name, name=tag)

            zf = zipfile.ZipFile('%s/data/2d/result_%s.zip' % (MEDIA_ROOT, job_id), 'w', zipfile.ZIP_DEFLATED)
            for f in glob.glob('%s/data/2d/result_%s/*' % (MEDIA_ROOT, job_id)):
                zf.write(f, os.path.basename(f))
            zf.close()
            shutil.rmtree('%s/data/2d/result_%s' % (MEDIA_ROOT, job_id))
            # subprocess.check_call('cd %s && zip -rm result_%s.zip result_%s' % (os.path.join(MEDIA_ROOT, 'data/2d/'), job_id, job_id), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        t_total = time.time() - t0
    except:
        t_total = time.time() - t0
        print "\033[41mError(s)\033[0m encountered: \033[94m", sys.exc_info()[0], "\033[0m"
        print traceback.format_exc()
        return create_err_html(job_id, t_total, 2)

    # when no solution found
    if (not plate.is_success):
        html = '<br/><hr/><div class="row"><div class="col-lg-8 col-md-8 col-sm-6 col-xs-6"><h2>Output Result:</h2></div><div class="col-lg-4 col-md-4 col-sm-6 col-xs-6"><h4 class="text-right"><span class="glyphicon glyphicon-search"></span>&nbsp;&nbsp;<span class="label label-violet">JOB_ID</span>: <span class="label label-inverse">%s</span></h4><button class="btn btn-blue pull-right" style="color: #ffffff;" title="Output in plain text" disabled><span class="glyphicon glyphicon-download-alt"></span>&nbsp;&nbsp;Save Result&nbsp;</button></div></div><br/><div class="alert alert-danger"><p><span class="glyphicon glyphicon-minus-sign"></span>&nbsp;&nbsp;<b>FAILURE</b>: No solution found (Primerize run finished without errors).<br/><ul><li>Please examine the primers input. Make sure the primer sequences and their order are correct, and their assembly match the full sequence. Try again with the correct input.</li><li>For further information, please feel free to <a class="btn btn-warning btn-sm" href="/about/#contact" style="color: #ffffff;"><span class="glyphicon glyphicon-send"></span>&nbsp;&nbsp;Contact&nbsp;</a> us to track down the problem.</li></ul></p>' % (job_id)
        if job_id != ARG['DEMO_2D_ID']:
            job_entry = Design2D.objects.get(job_id=job_id)
            job_entry.status = '3'
            job_entry.save()
        return create_res_html(html, job_id, 2)
    
    try:
        script = '<br/><hr/><div class="row"><div class="col-lg-8 col-md-8 col-sm-6 col-xs-6"><h2>Output Result:</h2></div><div class="col-lg-4 col-md-4 col-sm-6 col-xs-6"><h4 class="text-right"><span class="glyphicon glyphicon-search"></span>&nbsp;&nbsp;<span class="label label-violet">JOB_ID</span>: <span class="label label-inverse">%s</span></h4><a href="%s" class="btn btn-blue pull-right" style="color: #ffffff;" title="Output in plain text" download><span class="glyphicon glyphicon-download-alt"></span>&nbsp;&nbsp;Save Result&nbsp;</a></div></div><br/><div class="alert alert-default" title="Sequence Illustration"><p><span class="glyphicon glyphicon-question-sign"></span>&nbsp;&nbsp;<b>INFO</b>: <span class="monospace pull-right">__SEQ_ANNOT__</span></p></div>' % (job_id, '/site_data/2d/result_%s.zip' % job_id)
        script += '<div class="row"><div class="col-lg-10 col-md-10 col-sm-9 col-xs-9"><div class="alert alert-warning" id="col-res-l"><p>__NOTE_NUM__</p></div></div><div class="col-lg-2 col-md-2 col-sm-3 col-xs-3"><div class="alert alert-orange text-center" id="col-res-r"> <span class="glyphicon glyphicon-time"></span>&nbsp;&nbsp;<b>Time elapsed</b>:<br/><i>%.1f</i> s.</div></div></div>' % t_total

        script += '<div class="row"><div class="col-lg-12 col-md-12 col-sm-12 col-xs-12"><div class="panel panel-primary"><div class="panel-heading"><h2 class="panel-title"><span class="glyphicon glyphicon-th"></span>&nbsp;&nbsp;Plate Layout</h2></div><div class="panel-body">'
        json = {'plates': {}}
        flag = {}
        for i in xrange(plate.get('N_PLATE')):
            flag[i + 1] = []
            json['plates'][i + 1] = {'primers': {}}
            script += '<div class="row"><div class="col-lg-12 col-md-12 col-sm-12 col-xs-12"><p class="lead">Plate # <span class="label label-orange">%d</span></p></div></div><div class="row">' % (i + 1)

            for j in xrange(plate.get('N_PRIMER')):
                primer_sequences = plate._data['plates'][j][i]
                num_primers_on_plate = primer_sequences.get('count')

                if num_primers_on_plate:
                    if num_primers_on_plate < 24:
                        flag[i + 1].append((j + 1, num_primers_on_plate))

                    json['plates'][i + 1]['primers'][j + 1] = []
                    script += '<div class="col-lg-3 col-md-3 col-sm-4 col-xs-6"><div class="thumbnail"><div id="svg_plt_%d_prm_%d"></div><div class="caption"><p class="text-center center-block" style="margin-bottom:0px;"><i>Primer</i> <b>%d</b> %s</p></div></div></div>' % (i + 1, j + 1, j + 1, primer_suffix_html(j))

                    for k in xrange(96):
                        if primer_sequences._data.has_key(k + 1):
                            row = primer_sequences._data[k + 1]
                            json['plates'][i + 1]['primers'][j + 1].append({'coord': k + 1, 'label': row[0], 'pos': primerize.util.num_to_coord(k + 1), 'sequence': row[1]})
                        else:
                            json['plates'][i + 1]['primers'][j + 1].append({'coord': k + 1})

            script += '</div>'

        open(os.path.join(MEDIA_ROOT, 'data/2d/result_%s.json' % job_id), 'w').write(simplejson.dumps(json))
        script += '</div></div></div></div></div><div class="row"><div class="col-lg-12 col-md-12 col-sm-12 col-xs-12"><div class="panel panel-green"><div class="panel-heading"><h2 class="panel-title"><span class="glyphicon glyphicon-tasks"></span>&nbsp;&nbsp;Assembly Scheme</h2></div><div class="panel-body"><pre style="font-size:12px;">'
        if flag:
            warning = ''
            for key in flag.keys():
                if len(flag[key]):
                    warning += '<span class="glyphicon glyphicon-exclamation-sign"></span>&nbsp;&nbsp;<b>WARNING</b>: <i>Plate</i> #<span class="label label-orange">%d</span> ' % key
                    for p in xrange(len(flag[key])):
                        f = flag[key][p]
                        warning += '<i>Primer</i> <b>%d</b> %s, ' % (f[0], primer_suffix_html(f[0] - 1))
                    warning = warning[:-2]
                    warning += ' have fewer than <u>24</u> wells filled.<br/>'
            warning += '<span class="glyphicon glyphicon-info-sign"></span>&nbsp;&nbsp;<b>WARNING</b>: Group multiple plates that have fewer than <u>24</u> wells together before ordering.<br/>'
            script = script.replace('__NOTE_NUM__', warning)
        else:
            script = script.replace('<div class="alert alert-warning"><p>__NOTE_NUM__</p></div>', '<div class="alert alert-success"><p><span class="glyphicon glyphicon-ok-sign"></span>&nbsp;&nbsp;<b>SUCCESS</b>: All plates are ready to go. No editing is needed before placing the order.</p></div>')


        offset = plate.get('offset')        
        start = plate.get('which_muts')[0] + offset - 1
        end = plate.get('which_muts')[-1] + offset - 1
        fragments = []
        if start <= 20:
            fragments.append(plate.sequence[:start])
        else:
            fragments.append(plate.sequence[:10] + '......' + plate.sequence[start - 10:start])
        if end - start <= 40:
            fragments.append(plate.sequence[start:end + 1])
        else:
            fragments.append(plate.sequence[start:start + 20] + '......' + plate.sequence[end - 19:end + 1])
        if len(plate.sequence) - end <= 20:
            fragments.append(plate.sequence[end + 1:])
        else:
            fragments.append(plate.sequence[end + 1:end + 11] + '......' + plate.sequence[-10:])
        
        labels = ['%d' % (1 - offset), '%d' % plate.get('which_muts')[0], '%d' % plate.get('which_muts')[-1], '%d' % (len(plate.sequence) - offset)]
        (illustration_1, illustration_2, illustration_3) = ('', '', '')
        if len(fragments[0]) >= len(labels[0]):
            illustration_1 += '<span class="label-white label-default" style="color:#c28fdd;">' + fragments[0][0] + '</span><span class="label-white label-default">' + fragments[0][1:] + '</span>'
            illustration_2 += '<span style="color:#c28fdd;">|</span><span>%s</span>' % ('&nbsp;' * (len(fragments[0]) - 1))
            illustration_3 += '<span style="color:#c28fdd;">%s</span><span>%s</span>' % (labels[0], '&nbsp;' * (len(fragments[0]) - len(labels[0])))
        elif fragments[0]:
            illustration_1 += '<span class="label-white label-default" style="color:#c28fdd;">' + fragments[0][0] + '</span><span class="label-white label-default">' + fragments[0][1:] + '</span>'
            illustration_2 += '<span>%s</span>' % ('&nbsp;' * len(fragments[0]))
            illustration_3 += '<span>%s</span>' % ('&nbsp;' * len(fragments[0]))

        if len(fragments[1]) >= len(labels[1]) + len(labels[2]):
            illustration_1 += '<span class="label-green" style="color:#ff7c55;">' + fragments[1][0] + '</span><span class="label-green">' + fragments[1][1:-1] + '</span><span class="label-green" style="color:#ff7c55;">' + fragments[1][-1] + '</span>'
            illustration_2 += '<span style="color:#ff7c55;">|</span><span>%s</span><span style="color:#ff7c55;">|</span>' % ('&nbsp;' * (len(fragments[1]) - 2))
            illustration_3 += '<span style="color:#ff7c55;">%s</span><span>%s</span><span style="color:#ff7c55;">%s</span>' % (labels[1], '&nbsp;' * (len(fragments[1]) - len(labels[1]) - len(labels[2])), labels[2])
        elif fragments[1]:
            if len(fragments[1]) >= len(labels[1]):
                illustration_1 += '<span class="label-green" style="color:#ff7c55;">' + fragments[1][0] + '</span><span class="label-green">' + fragments[1][1:] + '</span>'
                illustration_2 += '<span style="color:#ff7c55;">|</span><span>%s</span>' % ('&nbsp;' * (len(fragments[1]) - 1))
                illustration_3 += '<span style="color:#ff7c55;">%s</span><span>%s</span>' % (labels[1], '&nbsp;' * (len(fragments[1]) - len(labels[1])))
            else:
                illustration_1 += '<span class="label-green">' + fragments[1] + '</span>'
                illustration_2 += '<span>%s</span>' % ('&nbsp;' * len(fragments[1]))
                illustration_3 += '<span>%s</span>' % ('&nbsp;' * len(fragments[1]))

        if len(fragments[2]) >= len(labels[3]):
            illustration_1 += '<span class="label-white label-default">' + fragments[2][:-1] + '</span><span class="label-white label-default" style="color:#c28fdd;">' + fragments[2][-1] + '</span>'
            illustration_2 += '<span>%s</span><span style="color:#c28fdd;">|</span>' % ('&nbsp;' * (len(fragments[2]) - 1))
            illustration_3 += '<span>%s</span><span style="color:#c28fdd;">%s</span>' % ('&nbsp;' * (len(fragments[2]) - len(labels[3])), labels[3])
        elif fragments[2]:
            illustration_1 += '<span class="label-white label-default">' + fragments[2][:-1] + '</span><span class="label-white label-default" style="color:#c28fdd;">' + fragments[2][-1] + '</span>'
            illustration_2 += '<span>%s</span>' % ('&nbsp;' * len(fragments[2]))
            illustration_3 += '<span>%s</span>' % ('&nbsp;' * len(fragments[2]))

        script = script.replace('__SEQ_ANNOT__', illustration_1 + '</p><p style="margin-top:0px;">&nbsp;<span class="monospace pull-right">' + illustration_2 + '</p><p style="margin-top:0px;">&nbsp;<span class="monospace pull-right">' + illustration_3)


        x = 0
        for line in plate._data['assembly'].print_lines:
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
                    Tm = '%2.1f' % plate._data['assembly'].Tm_overlaps[x]
                    x += 1
                    script += line[1].replace('x' * len(Tm), '<kbd>%s</kbd>' % Tm)
                elif '|' in line[1]:
                    script += line[1]
            script += '<br/>'
        script += '</pre></div></div></div></div><p class="lead"><span class="glyphicon glyphicon-question-sign"></span>&nbsp;&nbsp;<b><u><i>What\'s next?</i></u></b> Try our suggested experimental <a class="btn btn-info btn-sm" href="/protocol/#par_prep" role="button" style="color: #ffffff;"><span class="glyphicon glyphicon-file"></span>&nbsp;&nbsp;Protocol&nbsp;</a> for PCR assembly.</p><script type="text/javascript">resize();</script>'

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


def design_2d_from_1d(request):
    if request.META.has_key('HTTP_REFERER'):
        referer_job_id = request.META['HTTP_REFERER']
        referer_job_id = referer_job_id[referer_job_id.find('?job_id=') + 8:]

        form = Design2DForm()
        from_1d = False
        if Design1D.objects.filter(job_id=referer_job_id).exists():
            job_entry = Design1D.objects.get(job_id=referer_job_id)
            primers = job_entry.primers.replace('[', '').replace(']', '').replace("'", '').replace(' ', '')
            form = Design2DForm(initial={'sequence': job_entry.sequence, 'tag': job_entry.tag, 'primers': primers})
            from_1d = True
    else:
        return error400(request)

    return design_2d(request, form, from_1d)

