import cherrypy
from email.mime.text import MIMEText
import os
import smtplib
import string
import subprocess
import sys

from const import *
from config import *

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




