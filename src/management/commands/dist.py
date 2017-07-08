import os
import simplejson
import subprocess
import sys
import time
import traceback
import zipfile

from django.core.management.base import BaseCommand

from github import Github

from src.settings import *
# from src.models import SourceReleases


class Command(BaseCommand):
    help = 'Retrieves all code releases from Github as zip archives and update server code to latest.'

    def handle(self, *args, **options):
        t0 = time.time()
        self.stdout.write('%s:\t%s' % (time.ctime(), ' '.join(sys.argv)))

        flag = False
        try:
            gh = Github(login_or_token=GIT["ACCESS_TOKEN"])
            repo = GIT["DIST_REPO"]
            releases = gh.get_repo(repo).get_releases()

            result = []
            for rel in releases:
                ver = rel.tag_name
                if not os.path.exists('%s/dist/Primerize-%s.zip' % (MEDIA_ROOT, ver)):
                    subprocess.check_call('cd %s/dist && curl -J -L -H "Authorization: token %s" -o %s/dist/Primerize-%s.zip https://api.github.com/repos/%s/zipball/%s' % (MEDIA_ROOT, GIT["ACCESS_TOKEN"], MEDIA_ROOT, ver, repo, ver), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                    print "Release \033[94m%s\033[0m downloaded." % ver
                else:
                    print "Release \033[94m%s\033[0m already exists and is ignored." % ver

                result.append({'version': ver, 'title': rel.title, 'description': rel.body})

            simplejson.dump(result, open('%s/cache/stat_dist.json' % MEDIA_ROOT, 'w'), indent=' ' * 4, sort_keys=True)

            if os.path.exists('%s/dist/Primerize-master.zip' % MEDIA_ROOT):
                os.remove('%s/dist/Primerize-master.zip' % MEDIA_ROOT)
            subprocess.check_call('cd %s/dist && curl -J -L -H "Authorization: token %s" -o %s/dist/Primerize-master.zip https://api.github.com/repos/%s/zipball/master' % (MEDIA_ROOT, GIT["ACCESS_TOKEN"], MEDIA_ROOT, repo), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            print "Release \033[94mlatest master\033[0m downloaded."
            zf = zipfile.ZipFile('%s/dist/Primerize-master.zip' % MEDIA_ROOT, 'r')
            license = [name for name in zf.namelist() if 'LICENSE.md' in name]
            data = zf.read(license[0])
            open('%s/dist/Primerize-LICENSE.md' % MEDIA_ROOT, 'w').write(data)

        except Exception:
            self.stdout.write("    \033[41mERROR\033[0m: Failed to download release \033[94m%s\033[0m." % ver)
            err = traceback.format_exc()
            print err
            ts = '%s\t\t%s\n' % (time.ctime(), ' '.join(sys.argv))
            open('%s/cache/log_alert_admin.log' % MEDIA_ROOT, 'a').write(ts)
            open('%s/cache/log_cron_dist.log' % MEDIA_ROOT, 'a').write('%s\n%s\n' % (ts, err))
            flag = True

        if flag:
            self.stdout.write("Finished with errors!")
            self.stdout.write("Time elapsed: %.1f s." % (time.time() - t0))
            sys.exit(1)
        else:
            self.stdout.write("    \033[92mSUCCESS\033[0m: \033[94m%s\033[0m releases downloaded." % repo)
            self.stdout.write("Time elapsed: %.1f s." % (time.time() - t0))

