import subprocess

def get_jquery_ver():
    return subprocess.Popen('ls res/js/jquery-*.min.js', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].replace('res/js/jquery-', '').replace('.min.js', '').strip()


ARG = {
    'DEF_MIN_TM': 60.0,
    'DEF_MAX_LEN': 60,
    'DEF_MIN_LEN': 15,
    'DEF_NUM_PRM': -1,
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

    'JS_JQUERY': 'res/js/jquery-%s.min.js' % get_jquery_ver(),
    'JS_BOOTSTRAP': "res/js/bootstrap.min.js",
    'JS_ZEROCLIPBOARD': "res/js/ZeroClipboard.min.js",
    'JS_ADMIN': "res/js/_admin.js",
    'JS_CLIP': "res/js/_clip.js",
    'JS_DESIGN_1D': "res/js/_design_1d.js",
    'JS_DOWNLOAD_ERR': "res/js/_download_error.js",
    'JS_DOWNLOAD_LINK': "res/js/_download_link.js",
    'JS_DOWNLOAD': "res/js/_download.js",
    'JS_INDEX': "res/js/_index.js",
    'JS_LICENSE': "res/js/_license.js",
    'JS_PROTOCOL': "res/js/_protocol.js",
    'JS_TUTORIAL': "res/js/_tutorial.js",
    'JS_UTIL': "res/js/_util.js",

    'CSS_BOOTSTRAP': "res/css/bootstrap.min.css",
    'CSS_THEME': "res/css/theme.css",
    'CSS_PALETTE': "res/css/palette.css",
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

JOB_KEEP_EXPIRE = 90   

