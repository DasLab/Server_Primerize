import cherrypy
from email.mime.text import MIMEText
import os
import smtplib
import string
import subprocess
import sys

from const import *
from config import *


def get_first_part_of_page(sequence, tag, min_Tm, num_primers, max_length, min_length, is_num_primers, is_t7):
    script = load_html(PATH['DESIGN_1D'])
    if type(min_Tm) is float: min_Tm = str(min_Tm)
    if type(num_primers) is int: 
        num_primers = str(num_primers)
    elif type(num_primers) is list:
        num_primers = ''.join(num_primers)
    if type(max_length) is int: max_length = str(max_length)
    if type(min_length) is int: min_length = str(min_length)
    if "1" in is_num_primers:
        is_num_primers = "checked"
        is_num_primers_disabled = ""
    else:
        is_num_primers = ""
        is_num_primers_disabled = "disabled=\"disabled\""
    if "1" in is_t7:
        is_t7 = "checked"
    else:
        is_t7 = ""
    if num_primers in (str(ARG['DEF_NUM_PRM']), " ","auto", ""): num_primers = "auto"

    script = script.replace("__SEQ__", sequence).replace("__MIN_TM__", min_Tm).replace("__NUM_PRIMERS__", num_primers).replace("__MAX_LEN__", max_length).replace("__MIN_LEN__", min_length).replace("__TAG__", tag).replace("__LEN__", str(len(sequence))).replace("__IS_NUM_PRMS__", is_num_primers).replace("__IS_NUM_PRMS_DIS__", is_num_primers_disabled).replace("__IS_T7__", is_t7)
    return script


def is_valid_sequence(sequence):
    res = "A,G,C,U,T".split(",")
    for e in sequence.upper():
        if e not in SEQ['valid']:
            return 0
    return 1


def is_t7_present(sequence):
    is_G = 0
    if sequence[:20] == SEQ['T7']:
        if sequence[20:22] == 'GG': is_G = 1
        return (sequence, 1, is_G)
    else:
        if sequence[0:2] == 'GG': is_G = 1
        return (SEQ['T7'] + sequence, 0, is_G)


def create_res_html(html_content, job_id):
    f = open("cache/result_%s.html" % job_id, "w")
    f.write(html_content.encode('utf-8', 'ignore'))
    f.close()


def create_wait_html(sequence, tag, min_Tm, num_primers, max_length, min_length, is_num_primers, is_t7, job_id):
    script = "<br/><hr/><div class=\"container theme-showcase\"><div class=\"row\"><div class=\"col-md-8\"><h2>Output Result:</h2></div><div class=\"col-md-4\"><h4 class=\"text-right\"><span class=\"glyphicon glyphicon-search\"></span>&nbsp;&nbsp;<span class=\"label label-violet\">JOB_ID</span>: <span class=\"label label-inverse\">__JOB_ID___</span></h4><a href=\"__FILE_NAME__\" class=\"btn btn-blue pull-right\" style=\"color: #ffffff;\" title=\"Output in plain text\" download disabled>&nbsp;Save Result&nbsp;</a></div></div><br/><div class=\"progress\"><div class=\"progress-bar progress-bar-striped active\" role=\"progressbar\" aria-valuenow=\"100\" aria-valuemin=\"0\" aria-valuemax=\"100\" style=\"width: 100%\"><span class=\"sr-only\"></span></div></div><h3 class=\"modal-title\" id=\"myModalLabel\"><span class=\"glyphicon glyphicon-hourglass\"></span>&nbsp;&nbsp;Primerize is running...</h3><br/><p>Your query is being processed. Usually, the calculation is finished within 30 seconds. Depending on the input sequence length and complexity, the run may take longer.</p><p>You can close the browser and retrieve the result later using the above unique <span class=\"label label-violet\">JOB_ID</span>. The cached result expires after 3 months.</p></div>"
    script = script.replace("__JOB_ID___", job_id).replace("__FILE_NAME__", "/cache/result_%s.txt" % job_id)

    html_content = get_first_part_of_page(sequence, tag, min_Tm, num_primers, max_length, min_length, is_num_primers, is_t7).replace("__RESULT__", script)
    create_res_html(html_content, job_id)


def create_err_html(sequence, tag, min_Tm, num_primers, max_length, min_length, is_num_primers, is_t7, job_id):
    script = "<br/><hr/><div class=\"container theme-showcase\"><div class=\"row\"><div class=\"col-md-8\"><h2>Output Result:</h2></div><div class=\"col-md-4\"><h4 class=\"text-right\"><span class=\"glyphicon glyphicon-search\"></span>&nbsp;&nbsp;<span class=\"label label-violet\">JOB_ID</span>: <span class=\"label label-inverse\">__JOB_ID___</span></h4><a href=\"__FILE_NAME__\" class=\"btn btn-blue pull-right\" style=\"color: #ffffff;\" title=\"Output in plain text\" download disabled>&nbsp;Save Result&nbsp;</a></div></div><br/><div class=\"progress\"><div class=\"progress-bar progress-bar-danger progress-bar-striped\" role=\"progressbar\" aria-valuenow=\"100\" aria-valuemin=\"0\" aria-valuemax=\"100\" style=\"width: 100%\"><span class=\"sr-only\"></span></div></div><h3 class=\"modal-title\" id=\"myModalLabel\"><span class=\"glyphicon glyphicon-ban-circle\"></span>&nbsp;&nbsp;Primerize has difficulty in your query...</h3><br/><p>Primerize encountered an internal error while processing your query. Sorry for the inconvenience. </p><p>We will investigate and fix the problem.</p><p>For further information, please feel free to <a class=\"btn btn-warning btn-sm path_about\" href=\"#contact\" style=\"color: #ffffff;\">Contact</a> us to track down the problem.</p></div>"
    script = script.replace("__JOB_ID___", job_id).replace("__FILE_NAME__", "/cache/result_%s.txt" % job_id)

    script_500 = load_html(PATH['500'])
    script_500 = script_500[script_500.find("<div class=\"starter-template\">"):script_500.find("<div class=\"bs-docs-footer\"")]

    html_content = get_first_part_of_page(sequence, tag, min_Tm, num_primers, max_length, min_length, is_num_primers, is_t7).replace("__RESULT__", script + script_500)
    create_res_html(html_content, job_id)


def premature_return(msg, html_content, job_id):
    msg = "<br/><hr/><div class=\"container theme-showcase\"><h2>Output Result:</h2><div class=\"alert alert-danger\"><p><span class=\"glyphicon glyphicon-remove-sign\"></span>&nbsp;&nbsp;<b>ERROR</b>: " + msg + "</p></div>"
    html_content = html_content.replace("__RESULT__", msg)
    create_res_html(html_content, job_id)
    raise cherrypy.HTTPRedirect("result?job_id=%s" % job_id)


def get_full_sys_stat():
    ver = subprocess.Popen('uname -r | sed %s' % "'s/[a-z\-]//g'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip() + '\t'
    ver += '%s.%s.%s\t' % (sys.version_info.major, sys.version_info.minor, sys.version_info.micro)
    ver += cherrypy.__version__ + '\t'
    ver += subprocess.Popen('matlab -nojvm -nodisplay -nosplash -r "fprintf(version); exit();" | tail -1 | sed %s' % "'s/ (.*//g'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip().split('\n')[-1] + '\t'
    ver += subprocess.Popen('python -c "from rdatkit import settings; print settings.VERSION"', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip() + '\t'

    ver += subprocess.Popen('ls %s' % os.path.join(MEDIA_DIR, 'res/js/jquery-*.min.js'), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].replace(os.path.join(MEDIA_DIR, 'res/js/jquery-'), '').replace('.min.js', '').strip() + '\t'
    f = open(os.path.join(MEDIA_DIR, 'res/js/bootstrap.min.js'))
    f.readline()
    ver_bootstrap = f.readline()
    ver += ver_bootstrap[ver_bootstrap.find('v')+1: ver_bootstrap.find('(')].strip() + '\t'
    f.close()

    ver += subprocess.Popen('ssh -V 2> temp.txt && sed %s temp.txt | sed %s | sed %s | sed %s' % ("'s/^OpenSSH\_//g'", "'s/U.*//'", "'s/,.*//g'", "'s/[a-z]/./g'"), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip() + '\t'
    ver += subprocess.Popen('screen --version | sed %s | sed %s | sed %s' % ("'s/.*version//g'", "'s/(.*//g'", "'s/[a-z ]//g'"), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip() + '\t'
    ver += subprocess.Popen('tty --version | head -1 | sed %s' % "'s/.*) //g'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip() + '\t'

    ver += subprocess.Popen('apachectl -v | head -1 | sed %s | sed %s' % ("'s/.*\///g'", "'s/[a-zA-Z \(\)]//g'"), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip() + '\t'
    ver += subprocess.Popen("git --version | sed 's/.*version //g'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip() + '\t'

    ver += subprocess.Popen('gcc --version | head -1 | sed %s' % "'s/.*) //g'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip() + '\t'
    ver += subprocess.Popen('clang --version | head -1 | sed %s | sed %s' % ("'s/.*version //g'", "'s/[ (-].*//g'"), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip() + '\t'
    ver += subprocess.Popen('cmake --version | head -1 | sed %s | sed %s' % ("'s/.*version//g'", "'s/ //g'"), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip() + '\t'


    ver += subprocess.Popen('python -c "import numpy, scipy, matplotlib, celery, simplejson, setuptools, pip; print %s"' % "numpy.__version__, '\t', scipy.__version__, '\t', matplotlib.__version__, '\t', celery.__version__, '\t', simplejson.__version__, '\t', setuptools.__version__, '\t', pip.__version__", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip() + '\t'
    ver += subprocess.Popen('octave --version | head -1 | sed %s' % "'s/.*version //g'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip() + '\t'
    
    disk_sp = subprocess.Popen('df -h | head -2 | tail -1', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].split()
    ver += '%s / %s' % (disk_sp[3], disk_sp[2]) + '\t'
    if subprocess.Popen('uname', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip() == 'Darwin':
        mem_str = subprocess.Popen('top -l 1 | head -n 10 | grep PhysMem', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip()
        mem_avail = mem_str[mem_str.find(',')+1:mem_str.find('unused')].strip()
        mem_used = mem_str[mem_str.find(':')+1:mem_str.find('used')].strip()
    else:
        mem_str = subprocess.Popen('free -h', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip().split('\n')
        mem_avail = [x for x in mem_str[2].split(' ') if x][-1]
        mem_used = [x for x in mem_str[2].split(' ') if x][-2]
    ver += '%s / %s' % (mem_avail, mem_used) + '\t'

    ver += str(int(subprocess.Popen('ls -l %s | wc -l' % os.path.join(MEDIA_DIR, 'cache/'), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip()) - 1) + '\t'
    ver += subprocess.Popen('du -h %s' % os.path.join(MEDIA_DIR, 'cache/'), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip().split()[0] + '\t'

    ver += subprocess.Popen('pwd', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip() + '\t'
    ver += subprocess.Popen('find %s -name "NA_?hermo"' % os.path.abspath(".."), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip() + '\t'
    ver += subprocess.Popen('find %s -name "RDAT*Kit"' % os.path.abspath(".."), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip() + '\t'
    ver += subprocess.Popen('which python', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip() + '\t'
    ver += subprocess.Popen("which matlab | xargs ls -lah | sed 's/.*-> //g'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip()

    f = open('src/sys_ver.txt', 'w')
    f.write(ver)
    f.close()
    subprocess.Popen('rm temp.txt', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)


def send_email_notice(content):
    msg = MIMEText(content)
    msg['Subject']  = '[CherryPy] {primerize.stanford.edu} ERROR (EXTERNAL IP): Primerize error log'
    msg['To'] = ADMIN['email']
    msg['From'] = EMAIL['USER']

    s = smtplib.SMTP(EMAIL['HOST'], EMAIL['PORT'])
    s.starttls()
    s.login(EMAIL['USER'], EMAIL['PASSWORD'])
    s.sendmail(msg['From'], msg['To'], msg.as_string())
    s.quit()




