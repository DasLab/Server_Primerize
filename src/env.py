from django.shortcuts import render

import environ
import os
import simplejson

from config.t47_dev import *
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = IS_DEVEL


def reload_conf(DEBUG, MEDIA_ROOT):
    env = environ.Env(DEBUG=DEBUG,)  # set default values and casting
    environ.Env.read_env('%s/config/env.conf' % MEDIA_ROOT)  # reading .env file

    env_oauth = simplejson.load(open('%s/config/oauth.conf' % MEDIA_ROOT))
    AWS = env_oauth['AWS']
    GA = env_oauth['GA']
    DRIVE = env_oauth['DRIVE']
    GIT = env_oauth['GIT']
    APACHE_ROOT = '/var/www'

    env_arg = simplejson.load(open('%s/config/arg.conf' % MEDIA_ROOT))
    ARG = {
        'MIN_TM': env_arg['MIN_TM'],
        'MAX_LEN': env_arg['MAX_LEN'],
        'MIN_LEN': env_arg['MIN_LEN'],
        'NUM_PRM': env_arg['NUM_PRM'],

        'OFFSET': env_arg['OFFSET_P4P6'],
        'LIB': env_arg['LIB_P4P6'],
        'MIN_MUTS': env_arg['MIN_MUTS_P4P6'],
        'MAX_MUTS': env_arg['MAX_MUTS_P4P6'],

        'NUM_MUT': env_arg['NUM_MUT'],
        'IS_SINGLE': env_arg['IS_SINGLE'],
        'IS_FILLWT': env_arg['IS_FILLWT'],

        'DEMO_1D_ID': env_arg['DEMO_1D_ID'],
        'DEMO_2D_ID': env_arg['DEMO_2D_ID'],
        'DEMO_3D_ID_1': env_arg['DEMO_3D_ID_1'],
        'DEMO_3D_ID_2': env_arg['DEMO_3D_ID_2'],
    }
    SEQ = {
        'P4P6': env_arg['SEQ_P4P6'],
        'T7': env_arg['SEQ_T7'],
        'PRIMER_SET': env_arg['PRIMER_SET_P4P6'],
        'valid': env_arg['SEQ_VALID'],
    }
    STR = {
        'P4P6': env_arg['STR_P4P6'],
        'P4P6_1': env_arg['STR_P4P6_1'],
        'P4P6_2': env_arg['STR_P4P6_2'],
        'valid': env_arg['STR_VALID'],
    }

    env_cron = simplejson.load(open('%s/config/cron.conf' % MEDIA_ROOT))
    CRONJOBS = env_cron['CRONJOBS']
    CRONTAB_LOCK_JOBS = env_cron['CRONTAB_LOCK_JOBS']
    KEEP_BACKUP = env_cron['KEEP_BACKUP']
    KEEP_JOB = env_cron['KEEP_JOB']

    return (env, AWS, GA, DRIVE, GIT, APACHE_ROOT, ARG, SEQ, STR, CRONJOBS, CRONTAB_LOCK_JOBS, KEEP_BACKUP, KEEP_JOB)


class Singleton(object):
    """Base class for singleton pattern
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance


class SYS_PATH(Singleton):
    def __init__(self, MEDIA_ROOT):
        self.HTML_PATH = {
            'index': MEDIA_ROOT + '/media/html/public_index.html',
            'tutorial': MEDIA_ROOT + '/media/html/public_tutorial.html',
            'protocol': MEDIA_ROOT + '/media/html/public_protocol.html',
            'license': MEDIA_ROOT + '/media/html/public_license.html',
            'download': MEDIA_ROOT + '/media/html/public_download.html',
            'docs': MEDIA_ROOT + '/media/html/public_docs.html',
            'about': MEDIA_ROOT + '/media/html/public_about.html',
            'landing': MEDIA_ROOT + '/media/html/public_landing.html',

            'design_1d': MEDIA_ROOT + '/media/html/public_design_1d.html',
            'design_2d': MEDIA_ROOT + '/media/html/public_design_2d.html',
            'design_3d': MEDIA_ROOT + '/media/html/public_design_3d.html',

            'login': MEDIA_ROOT + '/media/html/user_login.html',
            'password': MEDIA_ROOT + '/media/html/user_password.html',

            'admin_apache': MEDIA_ROOT + '/media/html/admin_apache.html',
            'admin_aws': MEDIA_ROOT + '/media/html/admin_aws.html',
            'admin_ga': MEDIA_ROOT + '/media/html/admin_ga.html',
            'admin_git': MEDIA_ROOT + '/media/html/admin_git.html',
            'admin_backup': MEDIA_ROOT + '/media/html/admin_backup.html',
            'admin_dir': MEDIA_ROOT + '/media/html/admin_dir.html',
            'admin_doc': MEDIA_ROOT + '/media/html/admin_doc.html',
            'admin_man': MEDIA_ROOT + '/media/html/admin_man.html',
            'admin_ref': MEDIA_ROOT + '/media/html/admin_ref.html',

            '400': MEDIA_ROOT + '/media/html/error_400.html',
            '401': MEDIA_ROOT + '/media/html/error_401.html',
            '403': MEDIA_ROOT + '/media/html/error_403.html',
            '404': MEDIA_ROOT + '/media/html/error_404.html',
            '500': MEDIA_ROOT + '/media/html/error_500.html',
            '503': MEDIA_ROOT + '/media/html/error_503.html',
        }

        self.DATA_DIR = {
            'RESULT_1D_DIR': MEDIA_ROOT + '/data/1d/',
            'RESULT_2D_DIR': MEDIA_ROOT + '/data/2d/',
            'RESULT_3D_DIR': MEDIA_ROOT + '/data/3d/',

            'TMPDIR': MEDIA_ROOT + '/temp/',
        }


root = environ.Path(os.path.dirname(os.path.dirname(__file__)))
MEDIA_ROOT = root()
# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/"
PATH = SYS_PATH(MEDIA_ROOT)
# MEDIA_ROOT = os.path.join(os.path.abspath("."))
FILEMANAGER_STATIC_ROOT = root('media/admin') + '/'

(env, AWS, GA, DRIVE, GIT, APACHE_ROOT, ARG, SEQ, STR, CRONJOBS, CRONTAB_LOCK_JOBS, KEEP_BACKUP, KEEP_JOB) = reload_conf(DEBUG, MEDIA_ROOT)



def error400(request, status=True):
    status = (request.GET['status'].lower() != 'false') if 'status' in request.GET else status
    status = 400 if status else 200
    return render(request, PATH.HTML_PATH['400'], status=status)

def error401(request, status=True):
    status = (request.GET['status'].lower() != 'false') if 'status' in request.GET else status
    status = 401 if status else 200
    return render(request, PATH.HTML_PATH['401'], status=status)

def error403(request, status=True, reason=""):
    status = (request.GET['status'].lower() != 'false') if 'status' in request.GET else status
    status = 403 if status else 200
    return render(request, PATH.HTML_PATH['403'], status=status)

def error404(request, status=True):
    status = (request.GET['status'].lower() != 'false') if 'status' in request.GET else status
    status = 404 if status else 200
    return render(request, PATH.HTML_PATH['404'], status=status)

def error500(request, status=True):
    status = (request.GET['status'].lower() != 'false') if 'status' in request.GET else status
    status = 500 if status else 200
    return render(request, PATH.HTML_PATH['500'], status=status)

def error503(request, status=True):
    status = (request.GET['status'].lower() != 'false') if 'status' in request.GET else status
    status = 503 if status else 200
    return render(request, PATH.HTML_PATH['503'], status=status)

