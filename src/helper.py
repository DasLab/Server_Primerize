from django.http import HttpResponse

import binascii
import os
import re
import simplejson
import string

from src.settings import *
from src.models import *

import primerize
prm_1d = primerize.Primerize_1D
prm_2d = primerize.Primerize_2D
prm_3d = primerize.Primerize_3D


def random_job_id():
    while True:
        job_id = binascii.b2a_hex(os.urandom(8))
        try:
            is_exist = JobIDs.objects.get(job_id=job_id)
        except:
            return job_id


def is_valid_name(input, char_allow, length):
    if len(input) <= length: return 0
    src = ''.join([string.digits, string.ascii_letters, char_allow])
    for char in input:
        if char not in src: return 0
    return 1


def is_valid_email(input):
    input_split = input.split("@")
    if len(input_split) != 2: return 0
    if not is_valid_name(input_split[0], ".-_", 2): return 0
    input_split = input_split[1].split(".")
    if len(input_split) == 1: return 0
    for char in input_split:
        if not is_valid_name(char, "-", 1): return 0
    return 1


# def is_valid_sequence(sequence):
#     for e in sequence.upper():
#         if e in SEQ['valid']:
#             return 1
#     return 0


def is_t7_present(sequence):
    if sequence.startswith(SEQ['T7']):
        is_G = sequence[20:].startswith('GG')
        return (sequence, 1, is_G)
    else:
        is_G = sequence.startswith('GG')
        return (SEQ['T7'] + sequence, 0, is_G)


def form_data_clean_common(form_data):
    sequence = form_data['sequence']
    sequence = re.sub('[^' + ''.join(SEQ['valid']) + ']', '', sequence.upper().replace('U', 'T')).encode('utf-8', 'ignore')
    tag = form_data['tag']
    tag = re.sub('[^a-zA-Z0-9\ \.\-\_]', '', tag)
    if not tag: tag = 'primer'
    return (sequence, tag)


def form_data_clean_primers(primers):
    primers = re.sub('[^' + ''.join(SEQ['valid']) + ''.join(SEQ['valid']).lower() + '\ \,]', '', primers)
    primers = [str(p.strip()) for p in primers.split(',') if p.strip()]
    return primers


def form_data_clean_structures(structures):
    structures = re.sub('[^' + '\\'.join(STR['valid']) + '\ \,]', '', structures)
    structures = [str(s.strip()) for s in structures.split(',') if s.strip()]
    return structures


def form_data_clean_1d(form_data):
    min_Tm = form_data['min_Tm']
    max_len = form_data['max_len']
    min_len = form_data['min_len']
    num_primers = form_data['num_primers']
    is_num_primers = form_data['is_num_primers']
    is_check_t7 = form_data['is_check_t7']
    if not min_Tm: min_Tm = ARG['MIN_TM']
    if not max_len: max_len = ARG['MAX_LEN']
    if not min_len: min_len = ARG['MIN_LEN']
    if len(sequence) > 500: min_len = max(30, min_len)
    if (not num_primers) or (not is_num_primers): num_primers = ARG['NUM_PRM']
    return (min_Tm, max_len, min_len, num_primers, is_num_primers, is_check_t7)


def form_clean_data_2d(form_data, sequence):
    primers = form_data_clean_primers(form_data['primers'])
    offset = form_data['offset']
    min_muts = form_data['min_muts']
    max_muts = form_data['max_muts']
    lib = form_data['lib']
    if not offset: offset = 0
    (which_muts, min_muts, max_muts) = primerize.util.get_mut_range(min_muts, max_muts, offset, sequence)
    if not lib: lib = '1'
    which_lib = [int(lib)]
    return (primers, offset, min_muts, max_muts, which_muts, which_lib)


def form_clean_data_3d(form_data, sequence):
    (primers, offset, min_muts, max_muts, which_muts, which_lib) = form_clean_data_2d(form_data, sequence)
    structures = form_data_clean_structures(form_data['structures'])
    is_single = form_data['is_single']
    is_fill_WT = form_data['is_fill_WT']
    num_mutations = form_data['num_mutations']
    if not num_mutations: num_mutations = '1'
    num_mutations = int(num_mutations)
    return (primers, offset, min_muts, max_muts, which_muts, which_lib, structures, is_single, is_fill_WT, num_mutations)


def form_check_valid(type, sequence, num_primers=0, primers=[], min_muts=None, max_muts=None, structures=[]):
    if len(sequence) < 60:
        return HttpResponse(simplejson.dumps({'error': '10', 'type': type}, sort_keys=True, indent=' ' * 4), content_type='application/json')
    elif len(sequence) > 1000:
        return HttpResponse(simplejson.dumps({'error': '11', 'type': type}, sort_keys=True, indent=' ' * 4), content_type='application/json')
    elif num_primers % 2:
        return HttpResponse(simplejson.dumps({'error': '20', 'type': type}, sort_keys=True, indent=' ' * 4), content_type='application/json')

    if type >= 2:
        if type == 3:
            if not structures:
                return HttpResponse(simplejson.dumps({'error': '40', 'type': type}, sort_keys=True, indent=' ' * 4), content_type='application/json')
            len_str = map(len, structures)
            len_str = all([s == len(sequence) for s in len_str])
            if not len_str:
                return HttpResponse(simplejson.dumps({'error': '41', 'type': type}, sort_keys=True, indent=' ' * 4), content_type='application/json')

        if len(primers) % 2:
            return HttpResponse(simplejson.dumps({'error': '21', 'type': type}, sort_keys=True, indent=' ' * 4), content_type='application/json')
        elif min_muts > max_muts:
            return HttpResponse(simplejson.dumps({'error': '30', 'type': type}, sort_keys=True, indent=' ' * 4), content_type='application/json')

        if not primers:
            assembly = prm_1d.design(sequence)
            if assembly.is_success:
                primers = assembly.primer_set
            else:
                return HttpResponse(simplejson.dumps({'error': '01', 'type': type}, sort_keys=True, indent=' ' * 4), content_type='application/json')
    return (None, primers)


def primer_suffix_html(num):
    return '<span class="label label-danger">R</span>' if num % 2 else '<span class="label label-info">F</span>'


def create_res_html(html_content, job_id, type):
    open(MEDIA_ROOT + '/data/%dd/result_%s.html' % (type, job_id), 'w').write(html_content.encode('utf-8', 'ignore'))


def create_wait_html(job_id, type):
    html = '<br/><hr/><div class="row"><div class="col-lg-12 col-md-12 col-sm-12 col-xs-12"><h2><span class="glyphicon glyphicon-hourglass"></span>&nbsp;&nbsp;Primerize is running...  </h2></div></div><br/><div class="progress"><div class="progress-bar progress-bar-striped active" role="progressbar" aria-valuenow="100" aria-valuemin="0" aria-valuemax="100" style="width: 100%%;"><span class="sr-only"></span></div></div><h3 class="text-center">Your <span class="label label-violet">JOB_ID</span> is: <span class="label label-inverse">%s</span></h3><br/><br/><img class="center-block" src="/site_media/images/fg_loader.gif" width="48px" style="opacity:0.5;"/><br/><br/><div class="row"><div class="col-lg-6 col-md-6 col-sm-7 col-xs-7"><p>Your query is being processed. Usually, the calculation is finished within 30 seconds. Depending on the input sequence length and complexity, the run may take longer.</p><p>You can close the browser and retrieve the result later using the above unique <span class="label label-violet">JOB_ID</span>. The cached result expires after 9 months.</p></div><div class="col-lg-6 col-md-6 col-sm-5 col-xs-5"><p class="text-center well" ><b>Please <button id="btn-copy" class="btn btn-success" data-clipboard-target="#url_id"><span class="glyphicon glyphicon-copy"></span>&nbsp;&nbsp;Copy&nbsp;</button> this link: <br/><code id="url_id" style="word-wrap:break-word;">http://primerize.stanford.edu/result/?job_id=%s</code></b></p><br/></div><script type="text/javascript">var client = new Clipboard("#btn-copy");</script>' % (job_id, job_id)
    create_res_html(html, job_id, type)


def create_err_html(job_id, t_total, type):
    html = '<br/><hr/><div class="row"><div class="col-lg-8 col-md-8 col-sm-6 col-xs-6"><h2><span class="glyphicon glyphicon-ban-circle"></span>&nbsp;&nbsp;Primerize has difficulty in your query...</h2></div><div class="col-lg-4 col-md-4 col-sm-6 col-xs-6"><h4 class="text-right"><span class="glyphicon glyphicon-search"></span>&nbsp;&nbsp;<span class="label label-violet">JOB_ID</span>: <span class="label label-inverse">%s</span></h4><button class="btn btn-blue pull-right" style="color: #ffffff;" title="Output in plain text" disabled><span class="glyphicon glyphicon-download-alt"></span>&nbsp;&nbsp;Save Result&nbsp;</button></div></div><br/><div class="progress"><div class="progress-bar progress-bar-danger progress-bar-striped" role="progressbar" aria-valuenow="100" aria-valuemin="0" aria-valuemax="100" style="width: 100%%"><span class="sr-only"></span></div></div><br/><p>Primerize encountered an internal error while processing your query. Sorry for the inconvenience. </p><p>We will investigate and fix the problem.</p><p>For further information, please feel free to <a class="btn btn-warning btn-sm" href="/about/#contact" style="color: #ffffff;"><span class="glyphicon glyphicon-send"></span>&nbsp;&nbsp;Contact&nbsp;</a> us to track down the problem.</p>' % (job_id)
    if type == 1:
        job_entry = Design1D.objects.get(job_id=job_id)
    elif type == 2:
        job_entry = Design2D.objects.get(job_id=job_id)
    elif type == 3:
        job_entry = Design3D.objects.get(job_id=job_id)
    job_entry.status = '4'
    job_entry.time = t_total
    job_entry.save()

    script_500 = ''.join(open(PATH.HTML_PATH['500'], 'r').readlines())
    script_500 = script_500[script_500.find('<div class="row bgimg2-lg'):script_500.find('endblock') - 3]
    create_res_html(html + script_500, job_id, type)


