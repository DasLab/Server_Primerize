import os

MEDIA_ROOT = os.path.dirname(os.path.dirname(__file__))

class SYS_PATH:
    def __init__(self):
        self.HTML_PATH = {
            'index': MEDIA_ROOT + '/media/html/public_index.html',
            'tutorial': MEDIA_ROOT + '/media/html/public_tutorial.html',
            'protocol': MEDIA_ROOT + '/media/html/public_protocol.html',
            'license': MEDIA_ROOT + '/media/html/public_license.html',
            'download': MEDIA_ROOT + '/media/html/public_download.html',
            'about': MEDIA_ROOT + '/media/html/public_about.html',

            'design_1d': MEDIA_ROOT + '/media/html/public_design_1d.html',

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

