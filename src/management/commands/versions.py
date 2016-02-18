import os
import simplejson
import subprocess
import sys
import time
import traceback

from django.core.management.base import BaseCommand

from src.settings import *


class Command(BaseCommand):
    help = 'Collects system version information and outputs to cache/stat_sys.txt. Existing file will be overwritten.'

    def handle(self, *args, **options):
        t0 = time.time()
        self.stdout.write('%s:\t%s' % (time.ctime(), ' '.join(sys.argv)))

        d = time.strftime('%Y%m%d') #datetime.datetime.now().strftime('%Y%m%d')
        t = time.time()
        ver = {}
        self.stdout.write("Checking system versions...")

        try:
            cpu = subprocess.Popen("uptime | sed 's/.*: //g' | sed 's/,/ \//g'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip()

            ver['linux'] = subprocess.Popen("uname -r | sed 's/[a-z\-]//g'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip()
            ver['python'] = '%s.%s.%s' % (sys.version_info.major, sys.version_info.minor, sys.version_info.micro)
            ver['django'] = subprocess.Popen('python -c "import django; print django.__version__"', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip()

            open(os.path.join(MEDIA_ROOT, 'data/temp.txt'), 'w').write(subprocess.Popen('pip show django-crontab', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip())
            ver['django_crontab'] = subprocess.Popen("head -4 %s | tail -1 | sed 's/.*: //g'" % os.path.join(MEDIA_ROOT, 'data/temp.txt'), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip()
            open(os.path.join(MEDIA_ROOT, 'data/temp.txt'), 'w').write(subprocess.Popen('pip show django-environ', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip())
            ver['django_environ'] = subprocess.Popen("head -4 %s | tail -1 | sed 's/.*: //g'" % os.path.join(MEDIA_ROOT, 'data/temp.txt'), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip()

            ver['mysql'] = subprocess.Popen("mysql --version | sed 's/,.*//g' | sed 's/.*Distrib //g'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip()
            ver['apache'] = subprocess.Popen("apachectl -v | head -1 | sed 's/.*\///g' | sed 's/[a-zA-Z \(\)]//g'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip()
            if DEBUG:
                ver['mod_wsgi'] = 'N/A'
            else:
                ver['mod_wsgi'] = subprocess.Popen("apt-cache show libapache2-mod-wsgi | grep Version | head -1 | sed 's/.*: //g' | sed 's/-.*//g'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip()
            ver['openssl'] = subprocess.Popen("openssl version | sed 's/.*OpenSSL //g' | sed 's/[a-z].*//g'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip()

            ver_jquery = open(os.path.join(MEDIA_ROOT, 'media/js/jquery.min.js'), 'r').readline()
            ver['jquery'] = ver_jquery[ver_jquery.find('v')+1: ver_jquery.find('|')].strip()
            ver_bootstrap = open(os.path.join(MEDIA_ROOT, 'media/js/bootstrap.min.js'), 'r').readlines()
            ver_bootstrap = ver_bootstrap[1]
            ver['bootstrap'] = ver_bootstrap[ver_bootstrap.find('v')+1: ver_bootstrap.find('(')].strip()
            ver['django_suit'] = subprocess.Popen('python -c "import suit; print suit.VERSION"', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip()
            ver['django_adminplus'] = subprocess.Popen('python -c "import adminplus; print adminplus.__version__"', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip()
            if DEBUG:
                ver['django_filemanager'] = '0.0.2'
            else:
                open(os.path.join(MEDIA_ROOT, 'data/temp.txt'), 'w').write(subprocess.Popen('pip show django-filemanager', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip())
                ver['django_filemanager'] = subprocess.Popen("head -4 %s | tail -1 | sed 's/.*: //g'" % os.path.join(MEDIA_ROOT, 'data/temp.txt'), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip()

            ver_d3 = open(os.path.join(MEDIA_ROOT, 'media/js/d3.min.js'), 'r').readlines()
            ver_d3 = ''.join(ver_d3)
            ver_d3 = ver_d3[ver_d3.find('version:'):]
            ver['d3'] = ver_d3[9:ver_d3.find('"}')].strip()
            ver_zclip = open(os.path.join(MEDIA_ROOT, 'media/js/ZeroClipboard.min.js'), 'r').readlines()
            ver_zclip = ver_zclip[6]
            ver['zclip'] = ver_zclip[ver_zclip.find('v')+1:].strip()
            ver['gviz_api'] = '1.8.2'

            open(os.path.join(MEDIA_ROOT, 'data/temp.txt'), 'w').write(subprocess.Popen('ssh -V 2', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip())
            ver['ssh'] = subprocess.Popen("sed 's/^OpenSSH\_//g' %s | sed 's/U.*//' | sed 's/,.*//g' | sed 's/[a-z]/./g'" % os.path.join(MEDIA_ROOT, 'data/temp.txt'), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip()
            ver['git'] = subprocess.Popen("git --version | sed 's/.*version //g'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip()
            ver['llvm'] = subprocess.Popen("llvm-config --version", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip()
            ver['nano'] = subprocess.Popen("nano --version | head -1 | sed 's/.*version //g' | sed 's/(.*//g'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip()

            ver['gdrive'] = subprocess.Popen("drive -v | sed 's/.*v//g'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip()
            ver['zip'] = subprocess.Popen("zip -v | head -2 | tail -1 | sed 's/.*Zip //g' | sed 's/ (.*//g'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip()
            ver['curl'] = subprocess.Popen("curl --version | head -1 | sed 's/.*curl //g' | sed 's/ (.*//g'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip()

            ver['boto'] = subprocess.Popen('python -c "import boto; print boto.__version__"', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip()
            open(os.path.join(MEDIA_ROOT, 'data/temp.txt'), 'w').write(subprocess.Popen('pip show pygithub', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip())
            ver['pygithub'] = subprocess.Popen("head -4 %s | tail -1 | sed 's/.*: //g'" % os.path.join(MEDIA_ROOT, 'data/temp.txt'), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip()
            ver['xlwt']= subprocess.Popen('python -c "import xlwt; print xlwt.__VERSION__"', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip()
            ver['requests']= subprocess.Popen('python -c "import requests; print requests.__version__"', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip()
            ver['simplejson']= subprocess.Popen('python -c "import simplejson; print simplejson.__version__"', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip()
            ver['virtualenv']= subprocess.Popen('python -c "import virtualenv; print virtualenv.__version__"', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip()
            ver['pip']= subprocess.Popen('python -c "import pip; print pip.__version__"', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip()
            ver['numpy']= subprocess.Popen('python -c "import numpy; print numpy.__version__"', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip()
            ver['scipy']= subprocess.Popen('python -c "import scipy; print scipy.__version__"', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip()
            ver['matplotlib']= subprocess.Popen('python -c "import matplotlib; print matplotlib.__version__"', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip()
            ver['numba']= subprocess.Popen('python -c "import numba; print numba.__version__"', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip()

            ver['yuicompressor'] = subprocess.Popen("java -jar %s/../yuicompressor.jar -V" % MEDIA_ROOT, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip()

            ver['RDAT_Kit'] = subprocess.Popen('python -c "from rdatkit import settings; print settings.VERSION"', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip()
            ver['NA_Thermo'] = subprocess.Popen('python -c "import primerize; print primerize.__version__"', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip()

            disk_sp = subprocess.Popen('df -h | grep "/dev/"', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].split()
            ver['_disk'] = [disk_sp[3][:-1] + ' G', disk_sp[2][:-1] + ' G']
            if DEBUG:
                mem_str = subprocess.Popen('top -l 1 | head -n 10 | grep PhysMem', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip()
                mem_avail = mem_str[mem_str.find(',')+1:mem_str.find('unused')].strip()
                if 'M' in mem_avail: 
                    mem_avail = '%.1f G' % (int(mem_avail[:-1]) / 1024.)
                else:
                    mem_avail = mem_avail[:-1] + ' ' + mem_avail[-1]
                mem_used = mem_str[mem_str.find(':')+1:mem_str.find('used')].strip()
                if 'M' in mem_used: 
                    mem_used = '%.1f G' % (int(mem_used[:-1]) / 1024.)
                else:
                    mem_used = mem_used[:-1] + ' ' + mem_used[-1]
            else:
                mem_str = subprocess.Popen('free -h', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip().split('\n')
                mem_str = [x for x in mem_str[2].split(' ') if x]
                mem_avail = mem_str[-1]
                if mem_avail[-1] == 'G': 
                    mem_avail = str(float(mem_avail[:-1]) * 1024) + ' M'
                else:
                    mem_avail = mem_avail[:-1] + ' M'
                mem_used = mem_str[-2]
                if mem_used[-1] == 'G': 
                    mem_used = str(float(mem_used[:-1]) * 1024) + ' M'
                else:
                    mem_used = mem_used[:-1] + ' M'
            ver['_mem'] = [mem_avail, mem_used]
            ver['_cpu']= cpu.replace(' ', '').split('/')

            ver['_path'] = {
                'root' : MEDIA_ROOT,
                'data': MEDIA_ROOT + '/data',
                'media': MEDIA_ROOT + '/media',
                'NA_Thermo': '',
                'RDAT_Kit': ''
            }
            if DEBUG:
                ver['_path']['NA_Thermo'] = os.path.abspath(os.path.join(MEDIA_ROOT, '../../MATLAB_Code/NA_Thermo'))
                ver['_path']['RDAT_Kit'] = os.path.abspath(os.path.join(MEDIA_ROOT, '../../MATLAB_Code/RDAT_Kit'))
            else:
                ver['_path']['NA_Thermo'] = os.path.abspath(os.path.join(MEDIA_ROOT, '../NA_Thermo'))
                ver['_path']['RDAT_Kit'] = os.path.abspath(os.path.join(MEDIA_ROOT, '../RDAT_Kit'))

            gdrive_dir = 'echo'
            if not DEBUG: gdrive_dir = 'cd %s' % APACHE_ROOT
            prefix = ''
            if DEBUG: prefix = '_DEBUG'
            ver['_drive'] = subprocess.Popen("%s && drive quota | awk '{ printf $2 \" G\t\"}'" % gdrive_dir, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip().split('\t')

            open(os.path.join(MEDIA_ROOT, 'cache/stat_sys.json'), 'w').write(simplejson.dumps(ver, indent=' ' * 4, sort_keys=True))
            subprocess.Popen('rm %s' % os.path.join(MEDIA_ROOT, 'data/temp.txt'), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        except:
            err = traceback.format_exc()
            ts = '%s\t\t%s\n' % (time.ctime(), ' '.join(sys.argv))
            open('%s/cache/log_alert_admin.log' % MEDIA_ROOT, 'a').write(ts)
            open('%s/cache/log_cron_version.log' % MEDIA_ROOT, 'a').write('%s\n%s\n' % (ts, err))

            self.stdout.write("Finished with \033[41mERROR\033[0m!")
            self.stdout.write("Time elapsed: %.1f s." % (time.time() - t0))
            sys.exit(1)

        self.stdout.write("Time elapsed: %.1f s.\n" % (time.time() - t))
        self.stdout.write("\033[92mSUCCESS\033[0m: \033[94mVersions\033[0m recorded in cache/stat_sys.json.")
        self.stdout.write("All done successfully!")
        self.stdout.write("Time elapsed: %.1f s." % (time.time() - t0))

