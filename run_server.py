import cherrypy
import os
import re
import subprocess

from scipy.stats import *



MEDIA_DIR = os.path.join(os.path.abspath("."))

def get_first_part_of_page(sequence, min_Tm, num_primers, max_length, min_length):
    f = open(os.path.join(MEDIA_DIR, u'media/Design_result.html')) 
    lines = f.readlines()
    f.close()

    string = "".join(lines)
    if type(min_Tm) is float: min_Tm = str(min_Tm)
    if type(num_primers) is int: num_primers = str(num_primers)
    if type(max_length) is int: max_length = str(max_length)
    if type(min_length) is int: min_length = str(min_length)
    string = string.replace('__SEQ__', sequence).replace('__MIN_TM__', min_Tm).replace('__NUM_PRIMERS__', num_primers).replace('__MAX_LEN__', max_length).replace('__MIN_LEN__', min_length)
    return string


def is_valid_sequence(sequence):
	res = "A,G,C,U,T".split(",")
	for e in sequence.upper():
		if e not in res:
			return 0
	return 1


def display_complete_html(msg):
    msg += "</p></div></div><hr>"
    msg += "<footer class=\"bs-docs-footer\" role=\"contentinfo\"><div class=\"container\" class=\"row\"><div class=\"col-md-9\"><p class=\"muted credit\">Maintained by the <a href=\"http://daslab.stanford.edu\">Das Lab</a>, <a href=\"http://www.stanford.edu\">Stanford University</a>.<br><a href=\"/media/Download.html\">CopyRight</a> &copy 2008-2014 The Board of Trustees of the Leland Stanford Junior University. All Rights Reserved. </p></div><div class=\"col-md-3\"><p> powered by <a href=\"http://www.cherrypy.org/\">CherryPy</a> and <a href=\"http://getbootstrap.com/\">Bootstrap</a></p></div></div></footer></body></html>"
    return msg 


class rest:
    def __init__(self):
        pass


    @cherrypy.expose
    def index(self):
        return open(os.path.join(MEDIA_DIR, u'media/Design.html'))


    @cherrypy.expose
    def design_primers(self, sequence, is_agree, min_Tm, num_primers, max_length, min_length):

        if '1' not in is_agree:
            msg = "<div class=\"container theme-showcase\"><h2>Primerize output:</h2><div class=\"alert alert-danger\"><p><b>ERROR</b>: Terms and Conditions declined by user."
            return get_first_part_of_page(sequence, min_Tm, num_primers, max_length, min_length) + display_complete_html(msg)

        seq = sequence.upper().replace('U', 'T')
        sequence = ''
        for char in seq:
            if ord(char) not in (10, 13):
                sequence += char
        if len(sequence) < 60 or not is_valid_sequence(sequence):
            if not sequence:
                return get_first_part_of_page()
            msg = "<div class=\"container theme-showcase\"><h2>Primerize output:</h2><div class=\"alert alert-danger\"><p><b>ERROR</b>: Invalid sequence input."
            return get_first_part_of_page(sequence, min_Tm, num_primers, max_length, min_length) + display_complete_html(msg)


        try:
            min_Tm = float(min_Tm)
            if not num_primers:
                num_primers = -1
            else:
                num_primers = int(num_primers)
            max_length = int(max_length)
            min_length = int(min_length)
        except ValueError:
            msg = "<div class=\"container theme-showcase\"><h2>Primerize output:</h2><div class=\"alert alert-danger\"><p><b>ERROR</b>: Invalid advanced options input."
            return get_first_part_of_page(sequence, min_Tm, num_primers, max_length, min_length) + display_complete_html(msg)

        f_out = os.popen('matlab -nojvm -nodisplay -nosplash -r "design_primers(\'%s\',%d,%d,[],%d,%d,[],1); exit()"' % (sequence, min_Tm, num_primers, max_length, min_length))
        lines = f_out.readlines()
        f_out.close()

        lines = [line.replace('\n','') for line in lines]
        if lines[-2] and lines[-2][0] == '?':
            msg = "<div class=\"container theme-showcase\"><h2>Primerize output:</h2><div class=\"alert alert-danger\"><p><b>ERROR</b>: No solution found, please adjust advanced options."
            return get_first_part_of_page(sequence, min_Tm, num_primers, max_length, min_length) + display_complete_html(msg)

        sec_break = [i for i in range(len(lines)) if lines[i] == '#']
        self.lines_warning = lines[sec_break[0] : sec_break[1]]
        self.lines_primers = lines[sec_break[1] + 2 : sec_break[2]]
        self.lines_assembly = lines[sec_break[2] + 1 : -1]

        string = ""
        if self.lines_warning:
            string += "<div class=\"container theme-showcase\"><div class=\"row\"><div class=\"col-md-10\"><h2>Primerize output:</h2></div><div class=\"col-md-2\"><a href=\"primerize_result.txt\" class=\"btn btn-info pull-right\" download>&nbsp;Download&nbsp;</a></div></div><div class=\"alert alert-warning\" title=\"Mispriming alerts\"><p>"
            for line in self.lines_warning:
                if line[0] == '@':
                    string += "<b>WARNING</b>"
                    for char in line[8:]:
                        if char == 'F':
                            string += "</b><span class=\"label label-info\">"
                        elif char == 'R':
                            string += "</b><span class=\"label label-danger\">" 
                        elif char == '{':
                            string += "<font style=\"text-transform: uppercase;\"><b>"
                        elif char == '}':
                            string += "</span></font>"
                        elif char == '[':
                            string += "<span class=\"label label-success\">"
                        elif char == "]":
                            string += "</span>"
                        elif char == "(":
                            string += "<span class=\"label label-default\">"
                        elif char == ")":
                            string += "</span>"
                        else:
                            string += char 
                    string += "<br>"
        string +=  "</p></div><br>"

        string += "<div class=\"row\"><div class=\"panel panel-primary\"><div class=\"panel-heading\"><h2 class=\"panel-title\">Designed Primers</h2></div><div class=\"panel-body\"><table class=\"table\"><thead><tr><th class=\"col-md-1\">#</th><th class=\"col-md-1\">Length</th><th class=\"col-md-10\">Sequence</th></tr></thead><tbody>"
        for line in self.lines_primers:
            line = line.split('\t')
            num = "<b>" + line[0][7:]
            if int(line[0][7:]) % 2 == 0:
                num += " <span class=\"label label-danger\">R</span></b>"
            else:
                num += " <span class=\"label label-info\">F</span></b>"
            string += "<tr><td>" + num + "</td><td><em>" + line[1] + "</em></td><td>" + line[2] + "</td></tr>"

        string += "</tbody></table></div></div></div><div class=\"row\"><div class=\"panel panel-success\"><div class=\"panel-heading\"><h2 class=\"panel-title\">Assembly Scheme</h2></div><div class=\"panel-body\"><pre>"
        for line in self.lines_assembly:
            if line:
                if line[0] == '~':
                    string += "<span class=\"bg-primary\">" + line[1:] + "</span><br>"
                elif line[0] == '=':
                    string += "<span class=\"bg-warning\">" + line[1:] + "</span><br>"
                elif line[0] == '^':
                    for char in line[1:]:
                        if char in ('A','T','C','G'):
                            string += "<span class=\"bg-info\">" + char + "</span>"
                        else:
                            string += char
                    string += "<br>"
                elif line[0] == '!':
                    for char in line[1:]:
                        if char in ('A','T','C','G'):
                            string += "<span class=\"bg-danger\">" + char + "</span>"
                        else:
                            string += char
                    string += "<br>"
                else:
                    for char in line[1:]:
                        if char == '{':
                            string += "<kbd>"
                        elif char == '}':
                            string += "</kbd>" 
                        else:
                            string += char 
                    string += "<br>"
            else:
                string += "<br>"

        string += "</pre></div></div></div>"

        f = open('primerize_result.txt','w')
        f.write('#\n')
        for line in self.lines_warning:
            if line[0] == '@':
                f.write('%s\n' % line[1:].replace('{','').replace('}','').replace('(','').replace(')','').replace('[','').replace(']','').replace('Ff','').replace('Rr',''))
        f.write('#\n')
        for line in self.lines_primers:
            f.write('%s\n' % line)
        f.write('#\n')
        for line in self.lines_assembly:
            if line and line[0] in ('$','!','^','=','~'):
                f.write('%s\n' % line[1:].replace('{','').replace('}',''))
        f.close()

        return get_first_part_of_page(sequence, min_Tm, num_primers, max_length, min_length) + display_complete_html(string)


    @cherrypy.expose
    def example_P4P6(self):
        seq_P4P6='TTCTAATACGACTCACTATAGGCCAAAGGCGUCGAGUAGACGCCAACAACGGAAUUGCGGGAAAGGGGUCAACAGCCGUUCAGUACCAAGUCUCAGGGGAAACUUUGAGAUGGCCUUGCAAAGGGUAUGGUAAUAAGCUGACGGACAUGGUCCUAACCACGCAGCCAAGUCCUAAGUCAACAGAUCUUCUGUUGAUAUGGAUGCAGUUCAAAACCAAACCGUCAGCGAGUAGCUGACAAAAAGAAACAACAACAACAAC'
        return self.design_primers(seq_P4P6, "1", "60", "-1", "60", "15")    


    @cherrypy.expose
    def show_license(self):
        f = open(os.path.join(MEDIA_DIR, u'LICENSE.MD')) 
        lines = f.readlines()
        f.close()
        md = "".join([line.replace('\n','<br>') for line in lines]) + '</strong>'

        f = open(os.path.join(MEDIA_DIR, u'media/License.html')) 
        lines = f.readlines()
        f.close()
        string = "".join(lines)

        return string.replace('__LICENSE_CONTENT__', md)




if __name__ == "__main__":

    cherrypy.config.update( {
        #'server.socket_host':"171.64.65.150", 
        'server.socket_host':"127.0.0.1", 
        'server.socket_port':8080,
        'tools.staticdir.root': os.path.abspath(os.path.join(os.path.dirname(__file__), ''))
        #'tools.statiddir.root': "/Users/skullnite/Downloads"
    } )
    #print os.path.abspath(os.path.join(__file__, 'static'))
    #cherrypy.quickstart( rest(), '/', 'development.conf' )
    
    cherrypy.quickstart(rest(), '', config={
        '/css': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': 'css'
            },
        '/images': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': 'images'
            },
        '/media': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': 'media'
            },
        '/data': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': 'data'
            }
        }
    )





