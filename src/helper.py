import binascii
import os
import string


from src.settings import *
from src.models import *


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
        if not is_valid_name(char, "", 1): return 0
    return 1


# def is_valid_sequence(sequence):
#     for e in sequence.upper():
#         if e in SEQ['valid']:
#             return 1
#     return 0


def is_t7_present(sequence):
    if sequence[:20] == SEQ['T7']:
        is_G = (sequence[20:22] == 'GG')
        return (sequence, 1, is_G)
    else:
        is_G = (sequence[0:2] == 'GG')
        return (SEQ['T7'] + sequence, 0, is_G)


def primer_suffix_html(num):
    if num % 2:
        return '<span class="label label-danger">R</span>'
    else:
        return '<span class="label label-info">F</span>'


def random_job_id():
    return binascii.b2a_hex(os.urandom(8))


def create_res_html(html_content, job_id, type):
    open(MEDIA_ROOT + '/data/%dd/result_%s.html' % (type, job_id), 'w').write(html_content.encode('utf-8', 'ignore'))


def create_wait_html(job_id, type):
    html = '<br/><hr/><div class="row"><div class="col-md-12"><h2><span class="glyphicon glyphicon-hourglass"></span>&nbsp;&nbsp;Primerize is running...  </h2></div></div><br/><div class="progress"><div class="progress-bar progress-bar-striped active" role="progressbar" aria-valuenow="100" aria-valuemin="0" aria-valuemax="100" style="width: 100%%;"><span class="sr-only"></span></div></div><h3 class="text-center">Your <span class="label label-violet">JOB_ID</span> is: <span class="label label-inverse">%s</span></h3><br/><br/><img class="center-block" src="/site_media/images/fg_load.gif" width="48px" style="opacity:0.5;"/><br/><br/><div class="row"><div class="col-md-6"><p>Your query is being processed. Usually, the calculation is finished within 30 seconds. Depending on the input sequence length and complexity, the run may take longer.</p><p>You can close the browser and retrieve the result later using the above unique <span class="label label-violet">JOB_ID</span>. The cached result expires after 9 months.</p></div><div class="col-md-6"><p class="text-center well" ><b>Please <button id="btn-copy" class="btn btn-success" data-clipboard-text="http://primerize.stanford.edu/result/?job_id=%s"><span class="glyphicon glyphicon-copy"></span>&nbsp;&nbsp;Copy&nbsp;</button> this link: <br/><code id="url_id">http://primerize.stanford.edu/result/?job_id=%s</code></b></p><br/></div><script type="text/javascript">var client = new ZeroClipboard( document.getElementById("btn-copy") );</script>' % (job_id, job_id, job_id)
    create_res_html(html, job_id, type)


def create_err_html(job_id, t_total, type):
    html = '<br/><hr/><div class="row"><div class="col-md-8"><h2><span class="glyphicon glyphicon-ban-circle"></span>&nbsp;&nbsp;Primerize has difficulty in your query...</h2></div><div class="col-md-4"><h4 class="text-right"><span class="glyphicon glyphicon-search"></span>&nbsp;&nbsp;<span class="label label-violet">JOB_ID</span>: <span class="label label-inverse">%s</span></h4><button class="btn btn-blue pull-right" style="color: #ffffff;" title="Output in plain text" disabled><span class="glyphicon glyphicon-download-alt"></span>&nbsp;&nbsp;Save Result&nbsp;</button></div></div><br/><div class="progress"><div class="progress-bar progress-bar-danger progress-bar-striped" role="progressbar" aria-valuenow="100" aria-valuemin="0" aria-valuemax="100" style="width: 100%%"><span class="sr-only"></span></div></div><br/><p>Primerize encountered an internal error while processing your query. Sorry for the inconvenience. </p><p>We will investigate and fix the problem.</p><p>For further information, please feel free to <a class="btn btn-warning btn-sm" href="/about/#contact" style="color: #ffffff;"><span class="glyphicon glyphicon-send"></span>&nbsp;&nbsp;Contact&nbsp;</a> us to track down the problem.</p>' % (job_id)
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
    create_res_html(html+script_500, job_id, type)



