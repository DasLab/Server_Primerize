from django.http import HttpResponse

import binascii
import glob
import os
import re
import shutil
import simplejson
import string
import zipfile

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


def form_data_clean_1d(form_data, sequence):
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


def save_result_data(plate, job_id, tag, type):
    if plate.is_success:
        dir_name = os.path.join(MEDIA_ROOT, 'data/%dd/result_%s' % (type, job_id))
        if not os.path.exists(dir_name): os.mkdir(dir_name)
        plate.save('', path=dir_name, name=tag)

        zf = zipfile.ZipFile('%s/data/%dd/result_%s.zip' % (MEDIA_ROOT, type, job_id), 'w', zipfile.ZIP_DEFLATED)
        for f in glob.glob('%s/data/%dd/result_%s/*' % (MEDIA_ROOT, type, job_id)):
            zf.write(f, os.path.basename(f))
        zf.close()
        shutil.rmtree('%s/data/%dd/result_%s' % (MEDIA_ROOT, type, job_id))
        # subprocess.check_call('cd %s && zip -rm result_%s.zip result_%s' % (os.path.join(MEDIA_ROOT, 'data/2d/'), job_id, job_id), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)


def save_plate_json(json, job_id, type):
    simplejson.dump(json, open(os.path.join(MEDIA_ROOT, 'data/%dd/result_%s.json' % (type, job_id)), 'w'), sort_keys=True, indent=' ' * 4)


def primer_suffix_html(num):
    return '<span class="label label-danger">R</span>' if num % 2 else '<span class="label label-info">F</span>'


def output_header_html(job_id, type):
    url = '/site_data/1d/result_%s.txt' % job_id if type == 1 else '/site_data/%dd/result_%s.zip' % (type, job_id)
    return '<br/><hr/><div class="row"><div class="col-lg-8 col-md-8 col-sm-6 col-xs-6"><h2>Output Result:</h2></div><div class="col-lg-4 col-md-4 col-sm-6 col-xs-6"><h4 class="text-right"><span class="glyphicon glyphicon-search"></span>&nbsp;&nbsp;<span class="label label-violet">JOB_ID</span>: <span class="label label-inverse">%s</span></h4><a href="%s" class="btn btn-blue pull-right" style="color: #ffffff;" title="Output in plain text" download><span class="glyphicon glyphicon-download-alt"></span>&nbsp;&nbsp;Save Result&nbsp;</a></div></div><br/>' % (job_id, url)


def time_elapsed_html(t_total, type):
    alert = 'default' if type == 1 else 'warning'
    placeholder = '__NOTE_T7__' if type == 1 else '__NOTE_NUM__'
    return '<div class="row equal"><div class="col-lg-10 col-md-10 col-sm-9 col-xs-9"><div class="alert alert-%s"><p>%s</p></div></div><div class="col-lg-2 col-md-2 col-sm-3 col-xs-3"><div class="alert alert-orange text-center"> <span class="glyphicon glyphicon-time"></span>&nbsp;&nbsp;<b>Time elapsed</b>:<br/><i>%.1f</i> s.</div></div></div>' % (alert, placeholder, t_total)


def whats_next_html():
    return '<p class="lead"><span class="glyphicon glyphicon-question-sign"></span>&nbsp;&nbsp;<b><u><i>What\'s next?</i></u></b> Try our suggested experimental <a id="btn-result-to-protocol" class="btn btn-info btn-sm btn-spa" href="/protocol/#par_prep" role="button" style="color: #ffffff;"><span class="glyphicon glyphicon-file"></span>&nbsp;&nbsp;Protocol&nbsp;</a>'


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


def create_HTML_no_solution(job_id, type):
    if type == 1:
        html = '<br/><hr/><div class="row"><div class="col-lg-8 col-md-8 col-sm-6 col-xs-6"><h2>Output Result:</h2></div><div class="col-lg-4 col-md-4 col-sm-6 col-xs-6"><h4 class="text-right"><span class="glyphicon glyphicon-search"></span>&nbsp;&nbsp;<span class="label label-violet">JOB_ID</span>: <span class="label label-inverse">%s</span></h4><button class="btn btn-blue pull-right" style="color: #ffffff;" title="Output in plain text" disabled><span class="glyphicon glyphicon-download-alt"></span>&nbsp;&nbsp;Save Result&nbsp;</button></div></div><br/><div class="alert alert-danger"><p><span class="glyphicon glyphicon-minus-sign"></span>&nbsp;&nbsp;<b>FAILURE</b>: No solution found (Primerize run finished without errors).<br/><ul><li>Please examine the advanced options. Possible solutions might be restricted by stringent options combination, especially by minimum Tm and # number of primers. Try again with relaxed the advanced options.</li><li>Certain input sequence, e.g. polyA or large repeats, might be intrinsically difficult for PCR assembly design.</li><li>For further information, please feel free to <a class="btn btn-warning btn-sm" href="/about/#contact" style="color: #ffffff;"><span class="glyphicon glyphicon-send"></span>&nbsp;&nbsp;Contact&nbsp;</a> us to track down the problem.</li></ul></p></div>' % (job_id)
    else:
        html = '<br/><hr/><div class="row"><div class="col-lg-8 col-md-8 col-sm-6 col-xs-6"><h2>Output Result:</h2></div><div class="col-lg-4 col-md-4 col-sm-6 col-xs-6"><h4 class="text-right"><span class="glyphicon glyphicon-search"></span>&nbsp;&nbsp;<span class="label label-violet">JOB_ID</span>: <span class="label label-inverse">%s</span></h4><button class="btn btn-blue pull-right" style="color: #ffffff;" title="Output in plain text" disabled><span class="glyphicon glyphicon-download-alt"></span>&nbsp;&nbsp;Save Result&nbsp;</button></div></div><br/><div class="alert alert-danger"><p><span class="glyphicon glyphicon-minus-sign"></span>&nbsp;&nbsp;<b>FAILURE</b>: No solution found (Primerize run finished without errors).<br/><ul><li>Please examine the primers input. Make sure the primer sequences and their order are correct, and their assembly match the full sequence. Try again with the correct input.</li><li>For further information, please feel free to <a class="btn btn-warning btn-sm" href="/about/#contact" style="color: #ffffff;"><span class="glyphicon glyphicon-send"></span>&nbsp;&nbsp;Contact&nbsp;</a> us to track down the problem.</li></ul></p>' % (job_id)

    job_entry = []
    if type == 1 and job_id != ARG['DEMO_1D_ID']:
        job_entry = Design1D.objects.get(job_id=job_id)
    elif type == 2 and ARG['DEMO_2D_ID']:
        job_entry = Design2D.objects.get(job_id=job_id)
    elif type == 3 and job_id not in (ARG['DEMO_3D_ID_1'], ARG['DEMO_3D_ID_2']):
        job_entry = Design3D.objects.get(job_id=job_id)
    if job_entry:
        job_entry.status = '3'
        job_entry.save()
    return create_res_html(html, job_id, type)


def create_HTML_assembly(illustration):
    script = illustration.replace('->', '<span class="label-white label-orange glyphicon glyphicon-arrow-right" style="margin-left:2px; padding-left:1px;"></span>').replace('<-', '<span class="label-white label-green glyphicon glyphicon-arrow-left" style="margin-right:2px; padding-right:1px;"></span>').replace('\033[92m', '<span class="label-white label-primary">').replace('\033[96m', '<span class="label-warning">').replace('\033[94m', '<span class="label-info">').replace('\033[95m', '<span class="label-white label-danger">').replace('\033[41m', '<span class="label-white label-inverse">').replace('\033[100m', '<span style="font-weight:bold;">').replace('\033[0m', '</span>').replace('\n', '<br/>')
    script = '<div class="row"><div class="col-lg-12 col-md-12 col-sm-12 col-xs-12"><div class="panel panel-green"><div class="panel-heading"><h2 class="panel-title"><span class="glyphicon glyphicon-tasks"></span>&nbsp;&nbsp;Assembly Scheme</h2></div><div class="panel-body"><pre style="font-size:12px;">%s</pre></div></div></div></div>' % script
    return script


def create_HTML_primers(assembly):
    script = '<div class="row"><div class="col-lg-12 col-md-12 col-sm-12 col-xs-12"><div class="panel panel-primary"><div class="panel-heading"><h2 class="panel-title"><span class="glyphicon glyphicon-indent-left"></span>&nbsp;&nbsp;Designed Primers</h2></div><div class="panel-body"><table class="table table-striped table-hover" ><thead><tr class="active"><th class="col-lg-1 col-md-1 col-sm-1 col-xs-1">#</th><th class="col-lg-1 col-md-1 col-sm-1 col-xs-1">Length</th><th class="col-lg-10 col-md-10 col-sm-10 col-xs-10">Sequence</th></tr></thead><tbody>'
    for i, primer in enumerate(assembly.primer_set):
        script += '<tr><td><b>%d</b> %s</td><td><em>%d</em></td><td style="word-break:break-all" class="monospace">%s</td></tr>' % (i + 1, primer_suffix_html(i), len(primer), primer)

    script += '<tr><td colspan="3" style="padding: 0px;"></td></tr></tbody></table></div></div></div></div>'
    return script


def create_HTML_warnings(flag, script, type):
    if type == 1:
        warnings = flag.get('WARNING')
        if len(warnings):
            for w in warnings:
                p_1 = '<b>%d</b> %s' % (w[0], primer_suffix_html(w[0] - 1))
                p_2 = ', '.join('<b>%d</b> %s' % (x, primer_suffix_html(x - 1)) for x in w[3])
                script += '<span class="glyphicon glyphicon-exclamation-sign"></span>&nbsp;&nbsp;<b>WARNING</b>: Primer %s can misprime with <span class="label label-default">%d</span>-residue overlap to position <span class="label label-success">%s</span>, which is covered by primers: %s.<br/>' % (p_1, w[1], str(int(w[2])), p_2)
            script += '<span class="glyphicon glyphicon-info-sign"></span>&nbsp;&nbsp;<b>WARNING</b>: One-pot PCR assembly may fail due to mispriming; consider first assembling fragments in a preliminary PCR round (subpool).<br/>'
        else:
            script += '<span class="glyphicon glyphicon-ok-sign"></span>&nbsp;&nbsp;<b>SUCCESS</b>: No potential mis-priming found. See results below.<br/>'
            script = script.replace('alert-warning', 'alert-success')
        return script
    else:
        if flag:
            warning = ''
            for key in flag.keys():
                if len(flag[key]):
                    warning += '<span class="glyphicon glyphicon-exclamation-sign"></span>&nbsp;&nbsp;<b>WARNING</b>: <i>Plate</i> #<span class="label label-orange">%d</span> ' % key
                    for f in flag[key]:
                        warning += '<i>Primer</i> <b>%d</b> %s, ' % (f[0], primer_suffix_html(f[0] - 1))
                    warning = warning[:-2]
                    warning += ' have fewer than <u>24</u> wells filled.<br/>'
            warning += '<span class="glyphicon glyphicon-info-sign"></span>&nbsp;&nbsp;<b>WARNING</b>: Group multiple plates that have fewer than <u>24</u> wells together before ordering.<br/>'
            return script.replace('__NOTE_NUM__', warning)
        else:
            return script.replace('<div class="alert alert-warning"><p>__NOTE_NUM__</p></div>', '<div class="alert alert-success"><p><span class="glyphicon glyphicon-ok-sign"></span>&nbsp;&nbsp;<b>SUCCESS</b>: All plates are ready to go. No editing is needed before placing the order.</p></div>')


def create_HTML_t7_check(job_id, script, flag, is_t7, is_G):
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
    open(file_name, 'w').write(lines)
    return script.replace('__NOTE_T7__', str_t7.replace('\n', '<br/>').replace('T7_CHECK', '<b>T7_CHECK</b>').replace('SUCCESS', '<b>SUCCESS</b>').replace('WARNING', '<b>WARNING</b>').replace('NOT', '<u><b>NOT</b></u>').replace('nucleotides GG', 'nucleotides <u>GG</u>'))


def create_HTML_illustration(plate, script, type):
    if type == 2:
        (illustration_1, illustration_2, illustration_3) = plate._data['illustration']['lines']
    else:
        (illustration_3, illustration_2, illustration_1, illustration_str) = plate._data['illustration']['lines']
    illustration_1 = illustration_1.replace(' ', '&nbsp;').replace('\033[91m', '<span class="label-white label-default" style="color:#c28fdd;">').replace('\033[44m', '<span class="label-green" style="color:#ff7c55;">').replace('\033[46m', '<span class="label-green">').replace('\033[40m', '<span class="label-white label-default">').replace('\033[0m', '</span>')
    illustration_2 = illustration_2.replace(' ', '&nbsp;').replace('\033[92m', '<span style="color:#ff7c55;">').replace('\033[91m', '<span style="color:#c28fdd;">').replace('\033[0m', '</span>')
    illustration_3 = illustration_3.replace(' ', '&nbsp;').replace('\033[92m', '<span style="color:#ff7c55;">').replace('\033[91m', '<span style="color:#c28fdd;">').replace('\033[0m', '</span>')

    if type == 2:
        return script.replace('__SEQ_ANNOT__', illustration_1 + '</p><p class="text-right" style="margin-top:2px;">&nbsp;<span class="monospace">' + illustration_2 + '</p><p class="text-right" style="margin-top:0px;">&nbsp;<span class="monospace">' + illustration_3)
    else:
        illustration_str = illustration_str.replace(' ', '&nbsp;').replace('\033[43m', '<span class="label-white label-primary">').replace('\033[0m', '</span>')

        (illustration_str_annotated, illustration_1_annotated) = ('', '')
        num = 1 - plate._params['offset']
        for char in illustration_1:
            if char in ''.join(SEQ['valid']):
                illustration_1_annotated += '<span class="seqpos_%d">%s</span>' % (num, char)
                num += 1
            else:
                illustration_1_annotated += char

        for ill_str in illustration_str.split('\n'):
            num = 1 - plate._params['offset']
            for i, char in enumerate(ill_str):
                if char in ''.join(STR['valid']):
                    illustration_str_annotated += '<span class="seqpos_%d">%s</span>' % (num, char)
                    num += 1
                else:
                    illustration_str_annotated += char
            illustration_str_annotated += '<br/>'
        illustration_1 = illustration_1_annotated
        illustration_str = illustration_str_annotated[:-5] if len(plate.structures) >= 5 else illustration_str_annotated
        illustration_final = illustration_3 + '<br/>' + illustration_2 + '<br/>' + illustration_1 + '<br/><span style="white-space:pre;">' + illustration_str + '</span>'
        illustration_final = illustration_final + illustration_1 + '<br/><br/>' if len(plate.structures) >= 5 else illustration_final
        return script.replace('__SEQ_ANNOT__', illustration_final)


def create_HTML_plates(plate, script, job_id, type):
    script += '<div class="row"><div class="col-lg-12 col-md-12 col-sm-12 col-xs-12"><div class="panel panel-primary"><div class="panel-heading"><h2 class="panel-title"><span class="glyphicon glyphicon-th"></span>&nbsp;&nbsp;Plate Layout</h2></div><div class="panel-body">'
    json = {'plates': {}}
    primer_set = plate.primer_set
    flag = {}
    for i in xrange(plate.get('N_PLATE')):
        flag[i + 1] = []
        json['plates'][i + 1] = {'primers': {}}
        construct_list = primerize.Plate_96Well()
        script += '<div class="row"><div class="col-lg-12 col-md-12 col-sm-12 col-xs-12"><p class="lead">Plate # <span class="label label-orange">%d</span> <span style="font-size:small;">(<span class="glyphicon glyphicon-stats" style="color:#b7bac5;"></span> <u>__N_CONSTRUCT_PLATE__</u>)</span></p></div></div><div class="row">' % (i + 1)

        for j in xrange(plate.get('N_PRIMER')):
            primer_sequences = plate._data['plates'][j][i]
            num_primers_on_plate = len(primer_sequences)

            if num_primers_on_plate:
                if num_primers_on_plate == 1 and 'A01' in primer_sequences:
                    tag = primer_sequences.get('A01')[0]
                    if (isinstance(tag, primerize.Mutation) and not tag) or (isinstance(tag, str) and 'WT' in tag): continue

                if num_primers_on_plate < 24:
                    flag[i + 1].append((j + 1, num_primers_on_plate))

                json['plates'][i + 1]['primers'][j + 1] = []
                script += '<div class="col-lg-3 col-md-3 col-sm-4 col-xs-6"><div class="thumbnail"><div id="svg_plt_%d_prm_%d"></div><div class="caption"><p class="text-center center-block" style="margin-bottom:0px;"><i>Primer</i> <b>%d</b> %s <span style="font-size:small;">(<span class="glyphicon glyphicon-stats" style="color:#b7bac5;"></span> <u>%s</u>)</span></p></div></div></div>' % (i + 1, j + 1, j + 1, primer_suffix_html(j), num_primers_on_plate)

                for k in xrange(96):
                    if k + 1 in primer_sequences._data:
                        row = primer_sequences._data[k + 1]
                        if isinstance(row[0], primerize.Mutation):
                            lbl = ';'.join(row[0].list()) if row[0] else 'WT'
                            lbl = primer_sequences.tag + lbl
                        else:
                            lbl = row[0]
                        if row[1] == primer_set[j] and lbl != 'WT':
                            json['plates'][i + 1]['primers'][j + 1].append({'coord': k + 1, 'label': lbl, 'pos': primerize.util.num_to_coord(k + 1), 'sequence': row[1], 'color': 'green'})
                        else:
                            json['plates'][i + 1]['primers'][j + 1].append({'coord': k + 1, 'label': lbl, 'pos': primerize.util.num_to_coord(k + 1), 'sequence': row[1]})
                        construct_list.set(primerize.util.num_to_coord(k + 1), '', '')
                    else:
                        json['plates'][i + 1]['primers'][j + 1].append({'coord': k + 1})

        if not flag[i + 1]: del flag[i + 1]
        script += '</div>'
        script = script.replace('__N_CONSTRUCT_PLATE__', str(len(construct_list)))
    script += '</div></div></div></div></div>'

    save_plate_json(json, job_id, type)
    return (script, flag)

