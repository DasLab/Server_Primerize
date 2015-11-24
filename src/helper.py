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


def is_valid_sequence(sequence):
    for e in sequence.upper():
        if e in SEQ['valid']:
            return 1
    return 0


def is_t7_present(sequence):
    if sequence[:20] == SEQ['T7']:
        is_G = (sequence[20:22] == 'GG')
        return (sequence, 1, is_G)
    else:
        is_G = (sequence[0:2] == 'GG')
        return (SEQ['T7'] + sequence, 0, is_G)


def random_job_id():
    return binascii.b2a_hex(os.urandom(8))


def create_res_html(html_content, job_id):
    open(MEDIA_ROOT + '/data/1d/result_%s.html' % job_id, 'w').write(html_content.encode('utf-8', 'ignore'))


def create_wait_html(job_id):
    html = '<br/><hr/><div class="container theme-showcase"><div class="row"><div class="col-md-8"><h2>Output Result:</h2></div><div class="col-md-4"><h4 class="text-right"><span class="glyphicon glyphicon-search"></span>&nbsp;&nbsp;<span class="label label-violet">JOB_ID</span>: <span class="label label-inverse">%s</span></h4><a href="%s" class="btn btn-blue pull-right" style="color: #ffffff;" title="Output in plain text" download disabled>&nbsp;Save Result&nbsp;</a></div></div><br/><div class="progress"><div class="progress-bar progress-bar-striped active" role="progressbar" aria-valuenow="100" aria-valuemin="0" aria-valuemax="100" style="width: 100%%;"><span class="sr-only"></span></div></div><h3 class="modal-title" id="myModalLabel"><span class="glyphicon glyphicon-hourglass"></span>&nbsp;&nbsp;Primerize is running...</h3><br/><p>Your query is being processed. Usually, the calculation is finished within 30 seconds. Depending on the input sequence length and complexity, the run may take longer.</p><p>You can close the browser and retrieve the result later using the above unique <span class="label label-violet">JOB_ID</span>. The cached result expires after 3 months.</p></div>' % (job_id, '/site_data/1d/result_%s.txt' % job_id)
    create_res_html(html, job_id)


def create_err_html(job_id):
    html = '<br/><hr/><div class="container theme-showcase"><div class="row"><div class="col-md-8"><h2>Output Result:</h2></div><div class="col-md-4"><h4 class="text-right"><span class="glyphicon glyphicon-search"></span>&nbsp;&nbsp;<span class="label label-violet">JOB_ID</span>: <span class="label label-inverse">%s</span></h4><a href="%s" class="btn btn-blue pull-right" style="color: #ffffff;" title="Output in plain text" download disabled>&nbsp;Save Result&nbsp;</a></div></div><br/><div class="progress"><div class="progress-bar progress-bar-danger progress-bar-striped" role="progressbar" aria-valuenow="100" aria-valuemin="0" aria-valuemax="100" style="width: 100%%"><span class="sr-only"></span></div></div><h3 class="modal-title" id="myModalLabel"><span class="glyphicon glyphicon-ban-circle"></span>&nbsp;&nbsp;Primerize has difficulty in your query...</h3><br/><p>Primerize encountered an internal error while processing your query. Sorry for the inconvenience. </p><p>We will investigate and fix the problem.</p><p>For further information, please feel free to <a class="btn btn-warning btn-sm path_about" href="#contact" style="color: #ffffff;">Contact</a> us to track down the problem.</p></div>' % (job_id, '/site_data/1d/result_%s.txt' % job_id)
    job_entry = Design1D.objects.get(job_id=job_id)
    job_entry.status = 'error'
    job_entry.save()

    # script_500 = load_html(PATH['500'])
    # script_500 = script_500[script_500.find('<div class="starter-template">'):script_500.find('<div class="bs-docs-footer"')]

    # html_content = get_first_part_of_page(sequence, tag, min_Tm, num_primers, max_length, min_length, is_num_primers, is_t7).replace("__RESULT__", script + script_500)
    create_res_html(html, job_id)



