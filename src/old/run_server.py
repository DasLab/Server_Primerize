import binascii
import cherrypy
import glob
import os
import random
import re
import sys
import time

from const import *
from config import *
from helper import *
from wrapper import *


class Root:
    @cherrypy.expose
    def test_random(self):
        seq = SEQ['T7'] + ''.join(random.choice('CGTA') for _ in xrange(random.randint(100, 500)))
        return self.design_primers(seq, "scRNA", str(ARG['DEF_MIN_TM']), str(ARG['DEF_NUM_PRM']), str(ARG['DEF_MIN_LEN']), str(ARG['DEF_MAX_LEN']), "0", "1", binascii.b2a_hex(os.urandom(8)))

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
