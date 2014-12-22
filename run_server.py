import cherrypy
import glob
import os
import string
import subprocess
import sys
import tempfile
import time
# import re
# from scipy.stats import *

MEDIA_DIR = os.path.join(os.path.abspath("."))
DEF_MIN_TM = 60.0
DEF_MAX_LEN = 60
DEF_MIN_LEN = 15
DEF_NUM_PRM = -1
JOB_KEEP_EXPIRE = 7


def is_valid_name(input, char_allow, length):

    if len(input) <= length: return 0
    src = ''.join([string.digits, string.ascii_letters, char_allow])
    for char in input:
        if char not in src: return 0
    return 1


def is_valid_email(input):

    input_split = input.split("@")
    if len(input_split) != 2: return 0
    if not is_valid_name(input_split[0], ".-_", 2): return 0
    input_split = input_split[1].split(".")
    if len(input_split) == 1: return 0
    for char in input_split:
        if not is_valid_name(char, "", 1): return 0
    return 1


def get_first_part_of_page(sequence, tag, min_Tm, num_primers, max_length, min_length, is_num_primers):
    f = open("res/html/design_result.html") 
    lines = f.readlines()
    f.close()

    script = "".join(lines)
    if type(min_Tm) is float: min_Tm = str(min_Tm)
    if type(num_primers) is int: num_primers = str(num_primers)
    if type(max_length) is int: max_length = str(max_length)
    if type(min_length) is int: min_length = str(min_length)
    if "1" in is_num_primers:
        is_num_primers = "checked"
        is_num_primers_disabled = ""
    else:
        is_num_primers = ""
        is_num_primers_disabled = "disabled=\"disabled\""

    if num_primers in (str(DEF_NUM_PRM), " "): num_primers = "auto"
    script = script.replace("__SEQ__", sequence).replace("__MIN_TM__", min_Tm).replace("__NUM_PRIMERS__", num_primers).replace("__MAX_LEN__", max_length).replace("__MIN_LEN__", min_length).replace("__TAG__", tag).replace("__LEN__", str(len(sequence))).replace("__IS_NUM_PRMS__", is_num_primers).replace("__IS_NUM_PRMS_DIS__", is_num_primers_disabled)
    return script


def is_valid_sequence(sequence):
	res = "A,G,C,U,T".split(",")
	for e in sequence.upper():
		if e not in res:
			return 0
	return 1


def display_complete_html(msg):
    msg += "</p></div></div><hr/><div class=\"bs-docs-footer\" role=\"contentinfo\" id=\"footer\"></div></body></html>"
    return msg 


class rest:
    def __init__(self):
        pass


    @cherrypy.expose
    def index(self):
        return open("res/html/index.html")


    @cherrypy.expose
    def design_primers(self, sequence, tag, min_Tm, num_primers, max_length, min_length, is_num_primers):

        seq = sequence.upper().replace("U", "T")
        sequence = ""
        for char in seq:
            if ord(char) not in (10, 13, 32):
                sequence += char
        if len(sequence) < 60 or not is_valid_sequence(sequence):
            if not sequence:
                f = open("res/html/design.html")
                lines = f.readlines()
                f.close()
                script = "".join(lines)
                return script

            msg = "<div class=\"container theme-showcase\"><h2>Output Result:</h2><div class=\"alert alert-danger\"><p><b>ERROR</b>: Invalid sequence input."
            return get_first_part_of_page(sequence, tag, min_Tm, num_primers, max_length, min_length, is_num_primers) + display_complete_html(msg)


        try:
            min_Tm = float(min_Tm)

            if ("1" not in is_num_primers) or not num_primers or num_primers in (str(DEF_NUM_PRM), "auto"):
                num_primers = DEF_NUM_PRM
            else:
                num_primers = int(num_primers[0])
            max_length = int(max_length)
            min_length = int(min_length)
        except ValueError:
            msg = "<div class=\"container theme-showcase\"><h2>Output Result:</h2><div class=\"alert alert-danger\"><p><b>ERROR</b>: Invalid advanced options input."
            return get_first_part_of_page(sequence, tag, min_Tm, num_primers, max_length, min_length, is_num_primers) + display_complete_html(msg)
        if num_primers != DEF_NUM_PRM and num_primers % 2 != 0:
            msg = "<div class=\"container theme-showcase\"><h2>Output Result:</h2><div class=\"alert alert-danger\"><p><b>ERROR</b>: Invalid advanced options input: <b>#</b> number of primers must be <b><u>EVEN</u></b>."
            return get_first_part_of_page(sequence, tag, min_Tm, num_primers, max_length, min_length, is_num_primers) + display_complete_html(msg)
        if not tag: tag = "primer"

        t0 = time.time()
        f_run = subprocess.check_output(["matlab", "-nojvm", "-nodisplay", "-nosplash", "-r", "design_primers(\'%s\',%d,%d,[],%d,%d,[],1); exit()" % (sequence, min_Tm, num_primers, max_length, min_length)], shell=False)
        lines = f_run.split("\n")
        t_total = time.time() - t0

        lines = [line.replace("\n","") for line in lines]
        if lines[-2] and lines[-2][0] == "?":
            msg = "<div class=\"container theme-showcase\"><h2>Output Result:</h2><div class=\"alert alert-danger\"><p><b>ERROR</b>: No solution found, please adjust advanced options."
            return get_first_part_of_page(sequence, tag, min_Tm, num_primers, max_length, min_length, is_num_primers) + display_complete_html(msg)

        sec_break = [i for i in range(len(lines)) if lines[i] == "#"]
        self.lines_warning = lines[sec_break[0] : sec_break[1]]
        self.lines_primers = lines[sec_break[1] + 2 : sec_break[2]]
        self.lines_assembly = lines[sec_break[2] + 1 : -1]

        script = ""
        if self.lines_warning != ['#']:
            script += "<div class=\"container theme-showcase\"><div class=\"row\"><div class=\"col-md-10\"><h2>Output Result:</h2></div><div class=\"col-md-2\"><p class=\"text-right\"><b>Job ID</b>: __JOB_ID___</p><a href=\"__FILE_NAME__\" class=\"btn btn-info pull-right\" style=\"color: #ffffff;\" title=\"Output in plain text\" download>&nbsp;Save Result&nbsp;</a></div></div><br/><div class=\"alert alert-warning\" title=\"Mispriming alerts\"><p>"
            for line in self.lines_warning:
                if line[0] == "@":
                    script += "<b>WARNING</b>"
                    for char in line[8:]:
                        if char == "F":
                            script += "</b><span class=\"label label-info\">"
                        elif char == "R":
                            script += "</b><span class=\"label label-danger\">" 
                        elif char == "{":
                            script += "<font style=\"text-transform: uppercase;\"><b>"
                        elif char == "}":
                            script += "</span></font>"
                        elif char == "[":
                            script += "<span class=\"label label-success\">"
                        elif char == "]":
                            script += "</span>"
                        elif char == "(":
                            script += "<span class=\"label label-default\">"
                        elif char == ")":
                            script += "</span>"
                        else:
                            script += char 
                    script += "<br/>"
        else:
            script += "<div class=\"container theme-showcase\"><div class=\"row\"><div class=\"col-md-10\"><h2>Output Result:</h2></div><div class=\"col-md-2\"><p class=\"text-right\"><b>Job ID</b>: __JOB_ID___</p><a href=\"__FILE_NAME__\" class=\"btn btn-info pull-right\" title=\"Output in plain text\" download>&nbsp;Download&nbsp;</a></div></div><br/><div class=\"alert alert-success\" title=\"No alerts\"><p>"
            script += "<b>SUCCESS</b>: No potential mis-priming found. See results below."

        script +=  "</p></div><div class=\"row\"><div class=\"col-md-12\"><div class=\"alert alert-info\"> <b>Time elapsed</b>: %.1f" % t_total + " s.</div></div></div>"

        script += "<div class=\"row\"><div class=\"col-md-12\"><div class=\"panel panel-primary\"><div class=\"panel-heading\"><h2 class=\"panel-title\">Designed Primers</h2></div><div class=\"panel-body\"><table class=\"table table-hover\" ><thead><tr><th class=\"col-md-1\">#</th><th class=\"col-md-1\">Length</th><th class=\"col-md-10\">Sequence</th></tr></thead><tbody>"
        for line in self.lines_primers:
            line = line.split("\t")
            num = "<b>" + line[0][7:]
            if int(line[0][7:]) % 2 == 0:
                num = "<tr><td>" + num + "<span class=\"label label-danger\">R</span></b>"
            else:
                num = "<tr class=\"warning\"><td>" + num + "<span class=\"label label-info\">F</span></b>"
            script += num + "</td><td><em>" + line[1] + "</em></td><td style=\"word-break: break-all;\">" + line[2] + "</td></tr>"

        script += "</tbody></table></div></div></div></div><div class=\"row\"><div class=\"col-md-12\"><div class=\"panel panel-success\"><div class=\"panel-heading\"><h2 class=\"panel-title\">Assembly Scheme</h2></div><div class=\"panel-body\"><pre>"
        for line in self.lines_assembly:
            if line:
                if line[0] == "~":
                    script += "<span class=\"bg-primary\">" + line[1:] + "</span><br/>"
                elif line[0] == "=":
                    script += "<span class=\"bg-warning\">" + line[1:] + "</span><br/>"
                elif line[0] == "^":
                    for char in line[1:]:
                        if char in ("A","T","C","G"):
                            script += "<span class=\"bg-info\">" + char + "</span>"
                        else:
                            script += char
                    script += "<br/>"
                elif line[0] == "!":
                    for char in line[1:]:
                        if char in ("A","T","C","G"):
                            script += "<span class=\"bg-danger\">" + char + "</span>"
                        else:
                            script += char
                    script += "<br/>"
                else:
                    for char in line[1:]:
                        if char == "{":
                            script += "<kbd>"
                        elif char == "}":
                            script += "</kbd>" 
                        else:
                            script += char 
                    script += "<br/>"
            else:
                script += "<br/>"

        script += "</pre></div></div></div></div>"

        f = tempfile.NamedTemporaryFile(mode="w+b", prefix="result_", suffix=".txt", dir="cache", delete=False)
        file_name = f.name[-17:]

        f.write("Primerize Result\n\nINPUT\n=====\n%s\n" % sequence)
        f.write("#\nMIN_TM: %.1f\n" % min_Tm)
        if num_primers == DEF_NUM_PRM:
            f.write("NUM_PRIMERS: auto (unspecified)")
        else:
            f.write("NUM_PRIMERS: %d" % num_primers)
        f.write("\nMAX_LENGTH: %d\nMIN_LENGTH: %d\n" % (max_length, min_length))
        f.write("\n\nOUTPUT\n======\n")
        for line in self.lines_warning:
            if line[0] == "@":
                f.write("%s\n" % line[1:].replace("{","").replace("}","").replace("(","").replace(")","").replace("[","").replace("]","").replace("Ff","").replace("Rr",""))
        f.write("#\n")
        for line in self.lines_primers:
            f.write("%s\n" % line)
        f.write("#\n")
        for line in self.lines_assembly:
            if line and line[0] in ("$","!","^","=","~"):
                f.write("%s\n" % line[1:].replace("{","").replace("}",""))
        f.write("#\n\n------/* IDT USER: for primer ordering, copy and paste to Bulk Input */------\n------/* START */------\n")
        for line in self.lines_primers:
            line = line.split("\t")
            f.write("%s\t%s\t25nm\tSTD\n" % (line[0].replace("primer", tag), line[2]))
        f.write("------/* END */------\n------/* NOTE: use \"Lab Ready\" for \"Normalization\" */------\n")

        script = script.replace("__FILE_NAME__", u"cache/" + file_name).replace("__JOB_ID___", file_name[-10:-4])
        f.close()
        return get_first_part_of_page(sequence, tag, min_Tm, num_primers, max_length, min_length, is_num_primers) + display_complete_html(script)


    @cherrypy.expose
    def cleanup_old(self):
        older_7days = time.time() - JOB_KEEP_EXPIRE * 86400

        for f in glob.glob("cache/*.txt"):
            if (os.stat(f).st_mtime < older_7days):
                os.remove(f)


    @cherrypy.expose
    def example_P4P6(self):
        self.cleanup_old()
        seq_P4P6 = "TTCTAATACGACTCACTATAGGCCAAAGGCGUCGAGUAGACGCCAACAACGGAAUUGCGGGAAAGGGGUCAACAGCCGUUCAGUACCAAGUCUCAGGGGAAACUUUGAGAUGGCCUUGCAAAGGGUAUGGUAAUAAGCUGACGGACAUGGUCCUAACCACGCAGCCAAGUCCUAAGUCAACAGAUCUUCUGUUGAUAUGGAUGCAGUUCAAAACCAAACCGUCAGCGAGUAGCUGACAAAAAGAAACAACAACAACAAC"
        return self.design_primers(seq_P4P6, "P4P4_2HP", str(DEF_MIN_TM), str(DEF_NUM_PRM), str(DEF_MAX_LEN), str(DEF_MIN_LEN), "0")    


    @cherrypy.expose
    def show_license(self):
        f = open("LICENSE.MD") 
        lines = f.readlines()
        f.close()
        md = "".join([line.replace("\n","<br/>") for line in lines]) + "</strong>"

        f = open("res/html/license.html")
        lines = f.readlines()
        f.close()
        script = "".join(lines)

        return script.replace("__LICENSE_CONTENT__", md)


    @cherrypy.expose
    def submit_download(self, first_name, last_name, email, inst, dept, is_subscribe):

        is_valid = is_valid_name(first_name, "- ", 2) and is_valid_name(last_name, "- ", 2) and is_valid_name(inst, "()-, ", 4) and is_valid_name(dept, "()-, ", 4) and is_valid_email(email)

        if is_valid:
            f = open("src/usr_tab.csv", "a")
            if "1" in is_subscribe:
                f.write("1")
            else:
                f.write("0")
            f.write(",%s,%s,%s,%s,%s\n" % (first_name, last_name, email, inst, dept))
            f.close()

            f = open("res/html/download_link.html") 
            lines = f.readlines()
            f.close()
            script = "".join(lines)
            return script
        else:
            f = open("res/html/download_error.html") 
            lines = f.readlines()
            f.close()
            script = "".join(lines)
            script = script.replace("__F_NAME__", first_name).replace("__L_NAME__", last_name).replace("__EMAIL__", email).replace("__INST__", inst).replace("__DEPT__", dept)
            if "1" in is_subscribe: 
                script = script.replace("__IS_SUBSCRIBE__", "checked=\"yes\"") 
            else:
                script = script.replace("__IS_SUBSCRIBE__", "") 
            return script


if __name__ == "__main__":
    server_state = "dev"
    if len(sys.argv) > 1:
        server_state = sys.argv[1]
    if server_state not in ("dev","release"):
        print "Usage:\n\tpython run_server.py [flag]\n\n\tflag\t[required]\tuse \"release\" for hosting server\n\t\t\t\tuse \"dev\" for development test\n"
        raise SystemError("ERROR: Only can do development or release")
    if server_state == "release":
        socket_host = "171.65.23.206"
        socket_port = 8080
    else:
        socket_host = "127.0.0.1"
        socket_port = 8080

    cherrypy.config.update( {
        "server.socket_host":socket_host, 
        "server.socket_port":socket_port,
        "tools.staticdir.root": os.path.abspath(os.path.join(os.path.dirname(__file__), ""))
        #"tools.statiddir.root": "/Users/skullnite/Downloads"
    } )
    #print os.path.abspath(os.path.join(__file__, "static"))
    #cherrypy.quickstart( rest(), "/", "development.conf" )
    
    cherrypy.quickstart(rest(), "", config={
        "/res/css": {
            "tools.staticdir.on": True,
            "tools.staticdir.dir": "res/css"
            },
        "/res/js": {
            "tools.staticdir.on": True,
            "tools.staticdir.dir": "res/js"
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
            }
        }
    )

