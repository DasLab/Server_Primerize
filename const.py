import os
import subprocess

def get_jquery_ver():
    return subprocess.Popen('ls res/js/jquery-*.min.js', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].replace('res/js/jquery-', '').replace('.min.js', '').strip()


def load_html_parts(PATH):
    f = open(PATH['_NAVBAR'], "r")
    lines = f.readlines()
    f.close()
    script_navbar = "".join(lines)
    f = open(PATH['_FOOTER'], "r")
    lines = f.readlines()
    f.close()
    script_footer = "".join(lines)
    f = open(PATH['_MODAL'], "r")
    lines = f.readlines()
    f.close()
    script_modal = "".join(lines)
    f = open(PATH['_DEMO'], "r")
    lines = f.readlines()
    f.close()
    script_demo = "".join(lines)
    return (script_navbar, script_footer, script_modal, script_demo)


GA_TRACKER = "<script type=\"text/javascript\">(function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){(i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)})(window,document,'script','//www.google-analytics.com/analytics.js','ga'); ga('create', 'UA-36037648-2', 'auto'); ga('send', 'pageview'); </script>"


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

MEDIA_DIR = os.path.join(os.path.abspath("."))

PATH = {
    'DESIGN_1D': "res/html/design_1d.html",

    'HOME': "res/html/index.html",
    'TUTORIAL': "res/html/tutorial.html",
    'PROTOCOL': "res/html/protocol.html",
    'LICENSE': "res/html/license.html",
    'DOWNLOAD': "res/html/download.html",
    'ABOUT': "res/html/about.html",

    '_NAVBAR': "res/html/_navbar.html",
    '_FOOTER': "res/html/_footer.html",
    '_MODAL': "res/html/_modal.html",
    '_DEMO': "res/html/_demo.html",

    '403': "res/html/_403.html",
    '404': "res/html/_404.html",
    '500': "res/html/_500.html",
    'DEMO_1D_ERROR': "res/html/example_error.html",
    'DEMO_1D_FAIL': "res/html/example_fail.html",
    'DEMO_1D_WAIT': "res/html/example_wait.html",

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

(script_navbar, script_footer, script_modal, script_demo) = load_html_parts(PATH)


EMAIL = {
    'HOST': 'smtp.gmail.com',
    'USER': 'daslabsu@gmail.com',
    'PASSWORD': 'l4bd4s2014',
    'PORT': 587,    
}

ADMIN = {
    'email': 't47@stanford.edu',
    'login': {'daslab': EMAIL['PASSWORD']},
}

JOB_KEEP_EXPIRE = 90   

