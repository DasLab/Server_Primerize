import os
MEDIA_DIR = os.path.join(os.path.abspath("."))

import cherrypy
import traceback

from helper import load_html

from cherrypy.lib import auth_digest
USERS = {'daslab': 'labdas123'}

DEF_MIN_TM = 60.0
DEF_MAX_LEN = 60
DEF_MIN_LEN = 15
DEF_NUM_PRM = -1
JOB_KEEP_EXPIRE = 90

seq_P4P6 = "TTCTAATACGACTCACTATAGGCCAAAGGCGUCGAGUAGACGCCAACAACGGAAUUGCGGGAAAGGGGUCAACAGCCGUUCAGUACCAAGUCUCAGGGGAAACUUUGAGAUGGCCUUGCAAAGGGUAUGGUAAUAAGCUGACGGACAUGGUCCUAACCACGCAGCCAAGUCCUAAGUCAACAGAUCUUCUGUUGAUAUGGAUGCAGUUCAAAACCAAACCGUCAGCGAGUAGCUGACAAAAAGAAACAACAACAACAAC"
seq_T7 = "TTCTAATACGACTCACTATA"
seq_valid = ("A","T","C","G")

PATH_HOME = "res/html/index.html"
PATH_DESIGN = "res/html/design.html"
PATH_TUTORIAL = "res/html/tutorial.html"
PATH_PROTOCOL = "res/html/protocol.html"
PATH_LICENSE = "res/html/license.html"
PATH_DOWNLOAD = "res/html/download.html"
PATH_ABOUT = "res/html/about.html"

PATH_403 = "res/html/_403.html"
PATH_404 = "res/html/_404.html"
PATH_500 = "res/html/_500.html"
PATH_DEMO_ERROR = "res/html/example_error.html"
PATH_DEMO_FAIL = "res/html/example_fail.html"
PATH_DEMO_WAIT = "res/html/example_wait.html"

PATH_ADMIN = "res/html/admin.html"


def error_page_500():
    print traceback.format_exc()
    cherrypy.response.status = 500
    cherrypy.response.body = load_html(PATH_500)

def error_page_404(status, message, traceback, version):
    return load_html(PATH_404)

def error_page_403(status, message, traceback, version):
    return load_html(PATH_403)


QUICKSTART_CONFIG = {
        "/": {
            "tools.staticdir.root": MEDIA_DIR,
            "log.access_file": 'log_access.log',
            "log.error_file": 'log_error.log',
            'log.screen': False,
            'error_page.401': error_page_403,
            'error_page.403': error_page_403,
            'error_page.404': error_page_404,
            'request.error_response': error_page_500,
            'request.show_tracebacks': False,
            },
        "/res": {
            "tools.staticdir.on": True,
            "tools.staticdir.dir": "res"
            },
        "/cache": {
            "tools.staticdir.on": True,
            "tools.staticdir.dir": "cache"
            },

        "/src/primerize_release.zip": {
            "tools.staticfile.on": True,
            "tools.staticfile.filename": os.path.join(MEDIA_DIR, "src/primerize_release.zip")
            },
        "/LICENSE.md": {
            "tools.staticfile.on": True,
            "tools.staticfile.filename": os.path.join(MEDIA_DIR, "LICENSE.md")
            },
        "/robots.txt": {
            "tools.staticfile.on": True,
            "tools.staticfile.filename": os.path.join(MEDIA_DIR, "robots.txt")
            },

        '/admin': {
            'tools.auth_digest.on': True,
            'tools.auth_digest.realm': 'localhost',
            'tools.auth_digest.get_ha1': auth_digest.get_ha1_dict_plain(USERS),
            'tools.auth_digest.key': 'a565c27146791cfb'
           }
       }

