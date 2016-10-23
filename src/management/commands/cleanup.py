import datetime
import glob
import os
import sys
import time

from django.core.management.base import BaseCommand

from src.settings import *
from src.models import *
from src.console import send_notify_emails


class Command(BaseCommand):
    help = 'Cleans up old job results from database and folders.'

    def add_arguments(self, parser):
        parser.add_argument('--days', type=int, help='Days in the past considered obsolete, default 3 month is 90.')

    def handle(self, *args, **options):
        t0 = time.time()
        self.stdout.write('%s:\t%s' % (time.ctime(), ' '.join(sys.argv)))
        N_days = options['days'] if options['days'] else KEEP_JOB * 30

        t = time.time()
        self.stdout.write("Cleaning up obsolete job results...")

        all_job = JobIDs.objects.filter(date__range=(datetime.date(1970, 1, 2), datetime.date.today() - datetime.timedelta(days=N_days)))
        N_obsolete = 0

        for job in all_job:
            try:
                if job.type == '1':
                    obj = Design1D.objects.get(job_id=job.job_id)
                elif job.type == '2':
                    obj = Design2D.objects.get(job_id=job.job_id)
                elif job.type == '3':
                    obj = Design3D.objects.get(job_id=job.job_id)

                obj.delete()
                for f in glob.glob('%s/data/%sd/result_%s.*') % (MEDIA_ROOT, job.type, job.job_id):
                    os.remove(f)
            except Exception:
                pass

            job.delete()
            N_obsolete += 1


        all_files = set()
        N_orphan = 0
        for i in xrange(3):
            for f in glob.glob('%s/data/%sd/result_*.*' % (MEDIA_ROOT, i + 1)):
                all_files.add(f[f.find('/result_') - 2: f.rfind('.')])

        for f in all_files:
            job_id = f[f.find('result_') + 7:]
            job_type = f[:f.find('/') - 1]
            if job_type == '1':
                obj = Design1D.objects.filter(job_id=job_id)
            elif job_type == '2':
                obj = Design2D.objects.filter(job_id=job_id)
            elif job_type == '3':
                obj = Design3D.objects.filter(job_id=job_id)

            if not len(obj):
                for ff in glob.glob('%s/data/%s.*' % (MEDIA_ROOT, f)):
                    os.remove(ff)
                try:
                    job = JobIDs.objects.get(job_id=job_id)
                    job.delete()
                    N_orphan += 1
                except Exception:
                    pass

        self.stdout.write("    \033[92mSUCCESS\033[0m: \033[94m%s\033[0m obsolete job result files removed." % N_obsolete)
        self.stdout.write("    \033[92mSUCCESS\033[0m: \033[94m%s\033[0m orphan job result files removed." % N_orphan)
        self.stdout.write("Time elapsed: %.1f s.\n" % (time.time() - t))

        if not DEBUG:
            t_now = datetime.datetime.now().strftime('%b %d %Y (%a) @ %H:%M:%S')
            send_notify_emails('{%s} SYSTEM: Quarterly Cleanup Notice' % env('SERVER_NAME'), 'This is an automatic email notification for the success of scheduled quarterly cleanup of the %s Server local results.\n\nThe crontab job is scheduled at 00:00 (UTC) on 1st day of every 3 months.\n\nThe last system backup was performed at %s (PDT).\n\n%s Admin\n' % (env('SERVER_NAME'), t_now, env('SERVER_NAME')))
            self.stdout.write("Admin email (Quarterly Cleanup Notice) sent.")

        self.stdout.write("All done successfully!")
        self.stdout.write("Time elapsed: %.1f s." % (time.time() - t0))
