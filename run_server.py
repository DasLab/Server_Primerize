import binascii
import cherrypy
import glob
import os
import random
import sys
import time

from const import *
from config import *
from helper import *
from primerize import *


class Root:

    def __init__(self):
        pass

    @cherrypy.expose(['index'])
    def home(self):
        return load_html(PATH['HOME'])
    @cherrypy.expose(['help','intro'])
    def tutorial(self):
        return load_html(PATH['TUTORIAL'])
    @cherrypy.expose(['exp','experiment','resource'])
    def protocol(self):
        return load_html(PATH['PROTOCOL'])
    @cherrypy.expose(['readme','copyright'])
    def license(self):
        return load_html(PATH['LICENSE'])
    @cherrypy.expose(['package','repository'])
    def download(self):
        return load_html(PATH['DOWNLOAD']).replace("__SCRIPT__", '<script type="text/javascript" src="/' + PATH['JS_DOWNLOAD']+'"></script>')
    @cherrypy.expose(['citation','primerize','contact'])
    def about(self):
        return load_html(PATH['ABOUT']).replace("__HISTORY__", load_history())


    @cherrypy.expose(['find','retrieve'])
    def result(self, job_id):
        if not job_id: raise cherrypy.HTTPRedirect("home")
        file_name = "cache/result_%s.html" % job_id
        if os.path.exists(file_name):
            return load_html(file_name)
        else:
            raise cherrypy.NotFound()

    @cherrypy.expose(['design'])
    def design_1d(self):
        return load_html(PATH['DESIGN_1D']).replace("__SEQ__", "").replace("__MIN_TM__", str(ARG['DEF_MIN_TM'])).replace("__NUM_PRIMERS__", "auto").replace("__MAX_LEN__", str(ARG['DEF_MAX_LEN'])).replace("__MIN_LEN__", str(ARG['DEF_MIN_LEN'])).replace("__TAG__", "").replace("__LEN__", "0").replace("__IS_NUM_PRMS__", "").replace("__IS_NUM_PRMS_DIS__", "disabled=\"disabled\"").replace("__IS_T7__", "checked").replace("__RESULT__", "")
    @cherrypy.expose
    def design_primers(self, sequence, tag, min_Tm, num_primers, max_length, min_length, is_num_primers, is_t7, job_id):
        return design_primers(self, sequence, tag, min_Tm, num_primers, max_length, min_length, is_num_primers, is_t7, job_id)
    @cherrypy.expose(['demo','P4P6','demo_P4P6'])
    def demo_1d_P4P6(self):
        self.design_primers(SEQ['P4P6'], "P4P6_2HP", str(ARG['DEF_MIN_TM']), str(ARG['DEF_NUM_PRM']), str(ARG['DEF_MAX_LEN']), str(ARG['DEF_MIN_LEN']), "0", "1", binascii.b2a_hex(os.urandom(7)))    
    @cherrypy.expose
    def test_random(self):
        seq = SEQ['T7'] + ''.join(random.choice('CGTA') for _ in xrange(500))
        self.design_primers(seq, "scRNA", str(ARG['DEF_MIN_TM']), str(ARG['DEF_NUM_PRM']), str(ARG['DEF_MAX_LEN']), str(ARG['DEF_MIN_LEN']), "0", "1", binascii.b2a_hex(os.urandom(7)))  


    @cherrypy.expose
    def submit_download(self, first_name, last_name, email, inst, dept, is_subscribe):
        is_valid = is_valid_name(first_name, "- ", 2) and is_valid_name(last_name, "- ", 1) and is_valid_name(inst, "()-, ", 4) and is_valid_name(dept, "()-, ", 4) and is_valid_email(email)

        if is_valid:
            f = open("src/usr_tab.csv", "a")
            f.write("%s," % time.strftime("%c"))
            if "1" in is_subscribe:
                f.write("1")
            else:
                f.write("0")
            f.write(",%s,%s,%s,%s,%s\n" % (first_name, last_name, email, inst, dept))
            f.close()
            return load_html(PATH['DOWNLOAD']).replace("__SCRIPT__", '<script type="text/javascript" src="/' + PATH['JS_DOWNLOAD_LINK']+'"></script>')

        else:
            script = load_html(PATH['DOWNLOAD'])
            script = script.replace("__F_NAME__", first_name).replace("__L_NAME__", last_name).replace("__EMAIL__", email).replace("__INST__", inst).replace("__DEPT__", dept)
            if "1" in is_subscribe: 
                script = script.replace("__IS_SUBSCRIBE__", "checked=\"yes\"") 
            else:
                script = script.replace("__IS_SUBSCRIBE__", "") 
            return script.replace("__SCRIPT__", '<script type="text/javascript" src="/' + PATH['JS_DOWNLOAD_ERR']+'"></script>')


    @cherrypy.expose
    def error(self):
        raise ValueError
    @cherrypy.expose(['demo_error'])
    def demo_1d_error(self):
        return load_html(PATH['DEMO_1D_ERROR'])
    @cherrypy.expose(['demo_fail'])
    def demo_1d_fail(self):
        return load_html(PATH['DEMO_1D_FAIL'])
    @cherrypy.expose(['demo_wait'])
    def demo_1d_wait(self):
        return load_html(PATH['DEMO_1D_WAIT'])
    @cherrypy.expose
    def demo_404(self):
        return load_html(PATH['404'])
    @cherrypy.expose
    def demo_500(self):
        return load_html(PATH['500'])


    @cherrypy.expose
    def admin(self):
        script = load_html(PATH['ADMIN'])
        f = open('src/sys_ver.txt', 'r')
        (ver_linux, ver_python, ver_cherrypy, ver_matlab, ver_rdatkit, ver_jquery, ver_bootstrap, ver_ssh, ver_screen, ver_tty, ver_apache, ver_git, ver_gcc, ver_clang, ver_cmake, ver_numpy, ver_scipy, ver_matplotlib, ver_celery, ver_simplejson, ver_setuptools, ver_pip, ver_octave, disk_sp, mem_sp, cache_n, cache_sz, path_primerize, path_nathermo, path_rdatkit, path_python, path_matlab) = tuple(f.readlines()[0].split('\t'))
        f.close()

        script = script.replace("__LINUX_VER__", ver_linux).replace("__PYTHON_VER__", ver_python).replace("__CHERRYPY_VER__", ver_cherrypy).replace("__MATLAB_VER__", ver_matlab).replace("__RDATKIT_VER__", ver_rdatkit).replace("__JQUERY_VER__", ver_jquery).replace("__BOOTSTRAP_VER__", ver_bootstrap)
        script = script.replace("__SSH_VER__", ver_ssh).replace("__SCREEN_VER__", ver_screen).replace("__TTY_VER__", ver_tty).replace("__APACHE_VER__", ver_apache).replace("__GIT_VER__", ver_git).replace("__GCC_VER__", ver_gcc).replace("__CLANG_VER__", ver_clang).replace("__CMAKE_VER__", ver_cmake)
        script = script.replace("__NUMPY_VER__", ver_numpy).replace("__SCIPY_VER__", ver_scipy).replace("__MATPLOTLIB_VER__", ver_matplotlib).replace("__CELERY_VER__", ver_celery).replace("__SIMPLEJSON_VER__", ver_simplejson).replace("__SETUPTOOLS_VER__", ver_setuptools).replace("__PIP_VER__", ver_pip).replace("__OCTAVE_VER__", ver_octave)

        script = script.replace("__DISK_SP__", disk_sp).replace("__MEM_SP__", mem_sp).replace("__CACHE_SZ__", cache_sz).replace("__CACHE_N__", cache_n).replace("__PRIMERIZE_PATH__", path_primerize).replace("__NATHERMO_PATH__", path_nathermo).replace("__RDATKIT_PATH__", path_rdatkit).replace("__PYTHON_PATH__", path_python).replace("__MATLAB_PATH__", path_matlab)
        return script

    @cherrypy.expose
    def cleanup_old(self):
        older = time.time() - JOB_KEEP_EXPIRE * 86400

        for f in glob.glob("cache/*"):
            if (os.stat(f).st_mtime < older):
                os.remove(f)
        return self.get_sys()
    @cherrypy.expose
    def get_sys(self):
        get_full_sys_stat()
        return '<html><body onLoad="window.close()"></body></html>'
    @cherrypy.expose
    def ping_test(self):
        cherrypy.response.status = 200
        return ''


if __name__ == "__main__":
    server_state = "dev"
    if len(sys.argv) > 1:
        server_state = sys.argv[1]
    if server_state not in ("dev","release"):
        print "Usage:\n\tpython run_server.py [flag]\n\n\tflag\t[required]\tuse \"release\" for hosting server\n\t\t\t\tuse \"dev\" for development test\n"
        raise SystemError("ERROR: Only can do development or release")
    elif server_state != "release":
        cherrypy.config.update({
            "server.socket_host": "127.0.0.1",
            "server_state": 'dev',
        })

    cherrypy.quickstart(Root(), "", config=QUICKSTART_CONFIG)
    # wsgiapp = cherrypy.Application(StringGenerator(), '/', config=QUICKSTART_CONFIG)


