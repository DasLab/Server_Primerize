import os.path
import subprocess
import sys
import time
import traceback

from django.core.management.base import BaseCommand

from src.settings import *
from src.console import send_notify_emails


class Command(BaseCommand):
    help = 'Send email to admin of weekly aggregated errors and gzip the log_cron.log file.'

    def handle(self, *args, **options):
        t0 = time.time()
        self.stdout.write('%s:\t%s' % (time.ctime(), ' '.join(sys.argv)))

        try:
            if os.path.exists('%s/cache/log_alert_admin.log' % MEDIA_ROOT):
                lines = open('%s/cache/log_alert_admin.log' % MEDIA_ROOT, 'r').readlines()
                lines = ''.join(lines)
                send_notify_emails('[System] {%s} Weekly Error Report' % env('SSL_HOST'), 'This is an automatic email notification for the aggregated weekly error report. The following error occurred:\n\n\n%s\n\n\nDasLab Website Admin' % (lines))
                open('%s/cache/log_alert_admin.log' % MEDIA_ROOT, 'w').write('')
                self.stdout.write("\033[92mSUCCESS\033[0m: All errors were sent to \033[94mEmail\033[0m. Log cleared.")

            if os.path.exists('%s/cache/log_cron.log' % MEDIA_ROOT):
                subprocess.check_call('gzip -f %s/cache/log_cron.log' % MEDIA_ROOT, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                self.stdout.write("\033[92mSUCCESS\033[0m: \033[94mlog_cron.log\033[0m gzipped.")
            else:
                self.stdout.write("\033[92mSUCCESS\033[0m: \033[94mlog_cron.log\033[0m not exist, nothing to do.")
        except:
            err = traceback.format_exc()
            ts = '%s\t\t%s\n' % (time.ctime(), ' '.join(sys.argv))
            open('%s/cache/log_alert_admin.log' % MEDIA_ROOT, 'a').write(ts)
            open('%s/cache/log_cron_report.log' % MEDIA_ROOT, 'a').write('%s\n%s\n' % (ts, err))
            self.stdout.write("Finished with \033[41mERROR\033[0m!")
            self.stdout.write("Time elapsed: %.1f s." % (time.time() - t0))
            sys.exit(1)

        self.stdout.write("Finished with \033[92mSUCCESS\033[0m!")
        self.stdout.write("Time elapsed: %.1f s." % (time.time() - t0))
