import environ
import simplejson


def reload_conf(DEBUG, MEDIA_ROOT):
    env = environ.Env(DEBUG=DEBUG,) # set default values and casting
    environ.Env.read_env('%s/config/env.conf' % MEDIA_ROOT) # reading .env file

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

        'DEMO_1D_ID': env_arg['DEMO_1D_ID'],
        'DEMO_2D_ID': env_arg['DEMO_2D_ID'],
        'DEMO_3D_ID': env_arg['DEMO_3D_ID'],
    }
    SEQ = {
        'P4P6': env_arg['SEQ_P4P6'],
        'T7': env_arg['SEQ_T7'],
        'PRIMER_SET': env_arg['PRIMER_SET_P4P6'],
        'valid': env_arg['SEQ_VALID'],
    }

    env_cron = simplejson.load(open('%s/config/cron.conf' % MEDIA_ROOT))
    CRONJOBS = env_cron['CRONJOBS']
    CRONTAB_LOCK_JOBS = env_cron['CRONTAB_LOCK_JOBS']
    KEEP_BACKUP = env_cron['KEEP_BACKUP']
    KEEP_JOB = env_cron['KEEP_JOB']

    return (env, AWS, GA, DRIVE, GIT, APACHE_ROOT, ARG, SEQ, CRONJOBS, CRONTAB_LOCK_JOBS, KEEP_BACKUP, KEEP_JOB)


class SYS_PATH(object):
    def __init__(self, MEDIA_ROOT):
        self.HTML_PATH = {
            'index': MEDIA_ROOT + '/media/html/public_index.html',
            'tutorial': MEDIA_ROOT + '/media/html/public_tutorial.html',
            'protocol': MEDIA_ROOT + '/media/html/public_protocol.html',
            'license': MEDIA_ROOT + '/media/html/public_license.html',
            'download': MEDIA_ROOT + '/media/html/public_download.html',
            'about': MEDIA_ROOT + '/media/html/public_about.html',

            'design_1d': MEDIA_ROOT + '/media/html/public_design_1d.html',
            'design_2d': MEDIA_ROOT + '/media/html/public_design_2d.html',

            'login': MEDIA_ROOT + '/media/html/user_login.html',
            'password': MEDIA_ROOT + '/media/html/user_password.html',

            'admin_apache': MEDIA_ROOT + '/media/html/admin_apache.html',
            'admin_aws': MEDIA_ROOT + '/media/html/admin_aws.html',
            'admin_ga': MEDIA_ROOT + '/media/html/admin_ga.html',
            'admin_git': MEDIA_ROOT + '/media/html/admin_git.html',
            'admin_backup': MEDIA_ROOT + '/media/html/admin_backup.html',
            'admin_dir': MEDIA_ROOT + '/media/html/admin_dir.html',
            'admin_doc': MEDIA_ROOT + '/media/html/admin_doc.html',
            'admin_doc_old': MEDIA_ROOT + '/media/html/admin_doc_old.html',

            '400': MEDIA_ROOT + '/media/html/error_400.html',
            '401': MEDIA_ROOT + '/media/html/error_401.html',
            '403': MEDIA_ROOT + '/media/html/error_403.html',
            '404': MEDIA_ROOT + '/media/html/error_404.html',
            '500': MEDIA_ROOT + '/media/html/error_500.html',
        }

        self.DATA_DIR = {
            'RESULT_1D_DIR': MEDIA_ROOT + '/data/1d/',
            'RESULT_2D_DIR': MEDIA_ROOT + '/data/2d/',
            'RESULT_3D_DIR': MEDIA_ROOT + '/data/3d/',

            'TMPDIR': MEDIA_ROOT + '/temp/',
        }

