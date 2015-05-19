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
PATH_404 = "res/html/_404.html"
PATH_500 = "res/html/_500.html"

PATH_DEMO_ERROR = "res/html/example_error.html"
PATH_DEMO_FAIL = "res/html/example_fail.html"
PATH_DEMO_WAIT = "res/html/example_wait.html"

PATH_ADMIN = "res/html/admin.html"

QUICKSTART_CONFIG = {
        "/res/css": {
            "tools.staticdir.on": True,
            "tools.staticdir.dir": "res/css"
            },
        "/res/css/bootstrap": {
            "tools.staticdir.on": True,
            "tools.staticdir.dir": "res/css/bootstrap"
            },
        "/res/js": {
            "tools.staticdir.on": True,
            "tools.staticdir.dir": "res/js"
            },
        "/res/js/bootstrap": {
            "tools.staticdir.on": True,
            "tools.staticdir.dir": "res/js/bootstrap"
            },
        "/res/images": {
            "tools.staticdir.on": True,
            "tools.staticdir.dir": "res/images"
            },
        "/res/images/docs": {
            "tools.staticdir.on": True,
            "tools.staticdir.dir": "res/images/docs"
            },
        "/res/html": {
            "tools.staticdir.on": True,
            "tools.staticdir.dir": "res/html"
            },
        "/cache": {
            "tools.staticdir.on": True,
            "tools.staticdir.dir": "cache"
            },
            
        "/src/primerize_release.zip": {
            "tools.staticfile.on": True,
            "tools.staticfile.filename": "primerize_release.zip"
            },
        "/LICENSE.md": {
            "tools.staticfile.on": True,
            "tools.staticfile.filename": "LICENSE.md"
            },
        "/robots.txt": {
            "tools.staticfile.on": True,
            "tools.staticfile.filename": "robots.txt"
            }
        }

