import cherrypy
from cherrypy.lib import auth_digest
import os
import traceback

from const import *
from helper import load_html, send_email_notice


def secureheaders():
    headers = cherrypy.response.headers
    headers['X-Frame-Options'] = 'DENY'
    headers['X-XSS-Protection'] = '1; mode=block'
    headers['Content-Security-Policy'] = "default-src='self'"
cherrypy.tools.secureheaders = cherrypy.Tool('before_finalize', secureheaders)

def error_page_500():
    content = traceback.format_exc()
    if cherrypy.config.get('server_state') == "release": send_email_notice(content)
    cherrypy.response.status = 500
    cherrypy.response.body = load_html(PATH['500'])

def error_page_404(status, message, traceback, version):
    return load_html(PATH['404'])

def error_page_403(status, message, traceback, version):
    return load_html(PATH['403'])


MEDIA_DIR = os.path.join(os.path.abspath("."))
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

SERVER_IP = "171.65.23.206"
cherrypy.config.update({
    "server.socket_host": SERVER_IP,
    "server.socket_port": 8080,
    "server_state": 'release',
})
