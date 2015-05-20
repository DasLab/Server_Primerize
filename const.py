ARG = {
    'DEF_MIN_TM': 60.0,
    'DEF_MAX_LEN': 60,
    'DEF_MIN_LEN': 15,
    'DEF_NUM_PRM': -1,
    'JOB_KEEP_EXPIRE': 90,    
}

SEQ = {
    'P4P6': "TTCTAATACGACTCACTATAGGCCAAAGGCGUCGAGUAGACGCCAACAACGGAAUUGCGGGAAAGGGGUCAACAGCCGUUCAGUACCAAGUCUCAGGGGAAACUUUGAGAUGGCCUUGCAAAGGGUAUGGUAAUAAGCUGACGGACAUGGUCCUAACCACGCAGCCAAGUCCUAAGUCAACAGAUCUUCUGUUGAUAUGGAUGCAGUUCAAAACCAAACCGUCAGCGAGUAGCUGACAAAAAGAAACAACAACAACAAC",
    'T7': "TTCTAATACGACTCACTATA",
    'valid': ("A","T","C","G","U"),
}

PATH = {
    'HOME': "res/html/index.html",
    'DESIGN': "res/html/design.html",
    'TUTORIAL': "res/html/tutorial.html",
    'PROTOCOL': "res/html/protocol.html",
    'LICENSE': "res/html/license.html",
    'DOWNLOAD': "res/html/download.html",
    'ABOUT': "res/html/about.html",

    '403': "res/html/_403.html",
    '404': "res/html/_404.html",
    '500': "res/html/_500.html",
    'DEMO_ERROR': "res/html/example_error.html",
    'DEMO_FAIL': "res/html/example_fail.html",
    'DEMO_WAIT': "res/html/example_wait.html",

    'ADMIN': "res/html/admin.html",
}

EMAIL = {
    'HOST': 'smtp.gmail.com',
    'USER': 'stanfordrmdb@gmail.com',
    'PASSWORD': 'daslab4ever',
    'PORT': 587,    
}
ADMIN = {
    'email': 't47@stanford.edu',
    'login': {'daslab': EMAIL['PASSWORD']},
}


import os
MEDIA_DIR = os.path.join(os.path.abspath("."))

import cherrypy
from cherrypy.lib import auth_digest
import traceback

from helper import load_html, send_email_notice


def secureheaders():
    headers = cherrypy.response.headers
    headers['X-Frame-Options'] = 'DENY'
    headers['X-XSS-Protection'] = '1; mode=block'
    headers['Content-Security-Policy'] = "default-src='self'"
cherrypy.tools.secureheaders = cherrypy.Tool('before_finalize', secureheaders)

def error_page_500():
    content = traceback.format_exc()
    print content
    if cherrypy.config.get('server_state') == "release": send_email_notice(content)

    cherrypy.response.status = 500
    cherrypy.response.body = load_html(PATH['500'])

def error_page_404(status, message, traceback, version):
    return load_html(PATH['404'])

def error_page_403(status, message, traceback, version):
    return load_html(PATH['403'])


QUICKSTART_CONFIG = {
    "/": {
        "tools.staticdir.root": MEDIA_DIR,
        "tools.secureheaders.on": True,
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
        'tools.auth_digest.get_ha1': auth_digest.get_ha1_dict_plain(ADMIN['login']),
        'tools.auth_digest.key': 'a565c27146791cfb'
   }
}

