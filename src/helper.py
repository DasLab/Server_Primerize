import binascii
import glob
import os
import shutil
import simplejson
import zipfile

from src.settings import *

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


