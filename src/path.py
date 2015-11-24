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
            # 'lab_home': MEDIA_ROOT + '/media/html/group_index.html',
            # 'lab_meeting_schedule': MEDIA_ROOT + '/media/html/group_meeting_schedule.html',
            # 'lab_meeting_flash': MEDIA_ROOT + '/media/html/group_meeting_flash.html',
            # 'lab_meeting_jc': MEDIA_ROOT + '/media/html/group_meeting_jc.html',
            # 'lab_meeting_eterna': MEDIA_ROOT + '/media/html/group_meeting_eterna.html',
            # 'lab_meeting_rotation': MEDIA_ROOT + '/media/html/group_meeting_rotation.html',
            # 'lab_calendar': MEDIA_ROOT + '/media/html/group_calendar.html',
            # 'lab_resource_gdocs': MEDIA_ROOT + '/media/html/group_resource_document.html',
            # 'lab_resource_archive': MEDIA_ROOT + '/media/html/group_resource_archive.html',
            # 'lab_resource_contact': MEDIA_ROOT + '/media/html/group_resource_contact.html',
            # 'lab_server_aws': MEDIA_ROOT + '/media/html/group_server_aws.html',
            # 'lab_server_ga': MEDIA_ROOT + '/media/html/group_server_ga.html',
            # 'lab_service_git': MEDIA_ROOT + '/media/html/group_service_git.html',
            # 'lab_service_slack': MEDIA_ROOT + '/media/html/group_service_slack.html',
            # 'lab_service_dropbox': MEDIA_ROOT + '/media/html/group_service_dropbox.html',
            # 'lab_misc': MEDIA_ROOT + '/media/html/group_misc.html',
            # 'lab_error': MEDIA_ROOT + '/media/html/group_error.html',

            # 'admin_apache': MEDIA_ROOT + '/media/html/admin_apache.html',
            # 'admin_aws': MEDIA_ROOT + '/media/html/admin_aws.html',
            # 'admin_ga': MEDIA_ROOT + '/media/html/admin_ga.html',
            # 'admin_git': MEDIA_ROOT + '/media/html/admin_git.html',
            # 'admin_backup': MEDIA_ROOT + '/media/html/admin_backup.html',
            # 'admin_dir': MEDIA_ROOT + '/media/html/admin_dir.html',
            # 'admin_doc': MEDIA_ROOT + '/media/html/admin_doc.html',
            # 'admin_export': MEDIA_ROOT + '/media/html/admin_export.html',

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

