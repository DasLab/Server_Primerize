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

