import os
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
        self.stdout.write("Checking system versions...")

        try:
            cpu = subprocess.Popen("uptime | sed 's/.*: //g' | sed 's/,/ \//g'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip()

            ver = subprocess.Popen("uname -r | sed 's/[a-z\-]//g'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip() + '\t'
            ver += '%s.%s.%s\t' % (sys.version_info.major, sys.version_info.minor, sys.version_info.micro)
            ver += subprocess.Popen('python -c "import django; print django.__version__"', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip() + '\t'

            open(os.path.join(MEDIA_ROOT, 'data/temp.txt'), 'w').write(subprocess.Popen('pip show django-crontab', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip())
            ver += subprocess.Popen("head -4 %s | tail -1 | sed 's/.*: //g'" % os.path.join(MEDIA_ROOT, 'data/temp.txt'), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip() + '\t'
            open(os.path.join(MEDIA_ROOT, 'data/temp.txt'), 'w').write(subprocess.Popen('pip show django-environ', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip())
            ver += subprocess.Popen("head -4 %s | tail -1 | sed 's/.*: //g'" % os.path.join(MEDIA_ROOT, 'data/temp.txt'), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip() + '\t'

            ver += subprocess.Popen("mysql --version | sed 's/,.*//g' | sed 's/.*Distrib //g'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip() + '\t'
            ver += subprocess.Popen("apachectl -v | head -1 | sed 's/.*\///g' | sed 's/[a-zA-Z \(\)]//g'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip() + '\t'
            if DEBUG:
                ver += 'N/A\t'
            else:
                ver += subprocess.Popen("apt-cache show libapache2-mod-wsgi | grep Version | head -1 | sed 's/.*: //g' | sed 's/-.*//g'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip() + '\t'
            ver += subprocess.Popen("openssl version | sed 's/.*OpenSSL //g' | sed 's/[a-z].*//g'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip() + '\t'

            ver_jquery = open(os.path.join(MEDIA_ROOT, 'media/js/jquery.min.js'), 'r').readline()
            ver += ver_jquery[ver_jquery.find('v')+1: ver_jquery.find('|')].strip() + '\t'
            ver_bootstrap = open(os.path.join(MEDIA_ROOT, 'media/js/bootstrap.min.js'), 'r').readlines()
            ver_bootstrap = ver_bootstrap[1]
            ver += ver_bootstrap[ver_bootstrap.find('v')+1: ver_bootstrap.find('(')].strip() + '\t'
            ver += subprocess.Popen('python -c "import suit, adminplus; print %s"' % "suit.VERSION, '\t', adminplus.__version__", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip() + '\t'
            if DEBUG:
                ver += '0.0.2\t'
            else:
                open(os.path.join(MEDIA_ROOT, 'data/temp.txt'), 'w').write(subprocess.Popen('pip show django-filemanager', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip())
                ver += subprocess.Popen("head -4 %s | tail -1 | sed 's/.*: //g'" % os.path.join(MEDIA_ROOT, 'data/temp.txt'), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip() + '\t'

            ver_d3 = open(os.path.join(MEDIA_ROOT, 'media/js/d3.min.js'), 'r').readlines()
            ver_d3 = ''.join(ver_d3)
            ver_d3 = ver_d3[ver_d3.find('version:'):]
            ver += ver_d3[9:ver_d3.find('"}')].strip() + '\t'
            ver_zclip = open(os.path.join(MEDIA_ROOT, 'media/js/ZeroClipboard.min.js'), 'r').readlines()
            ver_zclip = ver_zclip[6]
            ver += ver_zclip[ver_zclip.find('v')+1:].strip() + '\t'
            ver += '1.8.2\t'

            open(os.path.join(MEDIA_ROOT, 'data/temp.txt'), 'w').write(subprocess.Popen('ssh -V 2', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip())
            ver += subprocess.Popen("sed 's/^OpenSSH\_//g' %s | sed 's/U.*//' | sed 's/,.*//g' | sed 's/[a-z]/./g'" % os.path.join(MEDIA_ROOT, 'data/temp.txt'), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip() + '\t'
            ver += subprocess.Popen("git --version | sed 's/.*version //g'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip() + '\t'
            ver += subprocess.Popen("llvm-config --version", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip() + '\t'
            ver += subprocess.Popen("nano --version | head -1 | sed 's/.*version //g' | sed 's/(.*//g'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip() + '\t'

            ver += subprocess.Popen("drive -v | sed 's/.*v//g'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip() + '\t'
            ver += subprocess.Popen("zip -v | head -2 | tail -1 | sed 's/.*Zip //g' | sed 's/ (.*//g'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip() + '\t'
            ver += subprocess.Popen("curl --version | head -1 | sed 's/.*curl //g' | sed 's/ (.*//g'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip() + '\t'

            ver += subprocess.Popen('python -c "import boto; print boto.__version__"', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip() + '\t'
            open(os.path.join(MEDIA_ROOT, 'data/temp.txt'), 'w').write(subprocess.Popen('pip show pygithub', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip())
            ver += subprocess.Popen("head -4 %s | tail -1 | sed 's/.*: //g'" % os.path.join(MEDIA_ROOT, 'data/temp.txt'), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip() + '\t'
            ver += subprocess.Popen('python -c "import virtualenv, pip, simplejson, requests, xlwt, numpy, scipy, matplotlib, numba; print %s"' % "xlwt.__VERSION__, '\t', requests.__version__, '\t', simplejson.__version__, '\t', virtualenv.__version__, '\t', pip.__version__, '\t', numpy.__version__, '\t', scipy.__version__, '\t', matplotlib.__version__, '\t', numba.__version__", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip() + '\t'

            ver += subprocess.Popen("java -jar %s/../yuicompressor.jar -V" % MEDIA_ROOT, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip() + '\t'

            ver += subprocess.Popen('python -c "from rdatkit import settings; print settings.VERSION"', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip() + '\t'
            ver += 'N/A\t'

            disk_sp = subprocess.Popen('df -h | grep "/dev/"', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].split()
            ver += '%s / %s' % (disk_sp[3][:-1] + ' G', disk_sp[2][:-1] + ' G') + '\t'
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
                mem_avail = [x for x in mem_str[2].split(' ') if x][-1][:-1] + ' M'
                mem_used = [x for x in mem_str[2].split(' ') if x][-2][:-1] + ' M'
            ver += '%s / %s' % (mem_avail, mem_used) + '\t'
            ver += subprocess.Popen('du -h --total %s | tail -1' % os.path.join(MEDIA_ROOT, 'backup/backup_*.*gz'), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip().split()[0] + '\t'
            ver += cpu + '\t'

            ver += '%s\t%s\t%s\t%s\t%s\t' % (MEDIA_ROOT, MEDIA_ROOT + '/data', MEDIA_ROOT + '/media', os.path.abspath(os.path.join(MEDIA_ROOT, '../NA_Thermo')), os.path.abspath(os.path.join(MEDIA_ROOT, '../RDAT_Kit')))

            gdrive_dir = 'echo'
            if not DEBUG: gdrive_dir = 'cd %s' % APACHE_ROOT
            prefix = ''
            if DEBUG: prefix = '_DEBUG'
            ver += subprocess.Popen("%s && drive quota | awk '{ printf $2 \" G\t\"}'" % gdrive_dir, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0]

            open(os.path.join(MEDIA_ROOT, 'cache/stat_sys.txt'), 'w').write(ver)
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
        self.stdout.write("\033[92mSUCCESS\033[0m: \033[94mVersions\033[0m recorded in cache/stat_sys.txt.")
        self.stdout.write("All done successfully!")
        self.stdout.write("Time elapsed: %.1f s." % (time.time() - t0))

