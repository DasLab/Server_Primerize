DEF_MIN_TM = 60.0
DEF_MAX_LEN = 60
DEF_MIN_LEN = 15
DEF_NUM_PRM = -1
JOB_KEEP_EXPIRE = 7

seq_P4P6 = "TTCTAATACGACTCACTATAGGCCAAAGGCGUCGAGUAGACGCCAACAACGGAAUUGCGGGAAAGGGGUCAACAGCCGUUCAGUACCAAGUCUCAGGGGAAACUUUGAGAUGGCCUUGCAAAGGGUAUGGUAAUAAGCUGACGGACAUGGUCCUAACCACGCAGCCAAGUCCUAAGUCAACAGAUCUUCUGUUGAUAUGGAUGCAGUUCAAAACCAAACCGUCAGCGAGUAGCUGACAAAAAGAAACAACAACAACAAC"
seq_T7 = "TTCTAATACGACTCACTATA"
seq_valid = ("A","T","C","G")

PATH_HOME = "res/html/index.html"
PATH_DESIGN = "res/html/design.html"
PATH_TUTORIAL = "res/html/tutorial.html"
PATH_LICENSE = "res/html/license.html"
PATH_DOWNLOAD = "res/html/download.html"
PATH_ABOUT = "res/html/about.html"
PATH_404 = "res/html/_404.html"
PATH_500 = "res/html/_500.html"

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
        "/res/html": {
            "tools.staticdir.on": True,
            "tools.staticdir.dir": "res/html"
            },
        "/cache": {
            "tools.staticdir.on": True,
            "tools.staticdir.dir": "cache"
            },
        "/src": {
            "tools.staticdir.on": True,
            "tools.staticdir.dir": "src"
            },
        "/": {
            "tools.staticdir.on": True,
            "tools.staticdir.dir": ""
            }
        }

