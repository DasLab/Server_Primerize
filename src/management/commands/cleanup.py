import datetime
import sys
import traceback

    # @cherrypy.expose
    # def cleanup_old(self):
    #     older = time.time() - JOB_KEEP_EXPIRE * 86400

    #     for f in glob.glob("cache/*"):
    #         if (os.stat(f).st_mtime < older):
    #             os.remove(f)
    #     return self.get_sys()

