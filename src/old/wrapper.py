import cherrypy
import subprocess
import time
import traceback

from const import *
from helper import *
from pymerize.primerize import *


def design_primers(self, sequence, tag, min_Tm, num_primers, max_length, min_length, is_num_primers, is_t7, job_id):
    html_content = get_first_part_of_page(sequence, tag, min_Tm, num_primers, max_length, min_length, is_num_primers, is_t7)
    seq = sequence.upper().replace('U', 'T')
    sequence = ''
    for char in seq:
        if ord(char) not in (10, 13, 32):
            sequence += char
    if len(sequence) < 60 or not is_valid_sequence(sequence):
        if not sequence:
            return self.design_1d()

        if len(sequence) < 60:
            msg = 'Invalid sequence input (should be <u>at least <b>60</b> nt</u> long).'
        else:
            msg = 'Invalid sequence input (should be composed of A, C, G, T and U).'
        premature_return(msg, html_content, job_id)
    else:            

        try:
            min_Tm = float(min_Tm)
            if ('1' not in is_num_primers) or not num_primers or num_primers in (str(ARG['DEF_NUM_PRM']), 'auto'):
                num_primers = ARG['DEF_NUM_PRM']
            else:
                if num_primers[0] == 'auto':
                    num_primers = ARG['DEF_NUM_PRM']
                else:
                    num_primers = int(num_primers[0])
            max_length = int(max_length)
            min_length = int(min_length)
        except ValueError:
            if not (type(num_primers) is int): num_primers = num_primers[0]
            msg = 'Invalid advanced options input.'
            premature_return(msg, html_content, job_id)
        if num_primers != ARG['DEF_NUM_PRM'] and num_primers % 2 != 0:
            msg = 'Invalid advanced options input: <b>#</b> number of primers must be <b><u>EVEN</u></b>.'
            premature_return(msg, html_content, job_id)
        if '1' in is_t7: (sequence, flag, is_G) = is_t7_present(sequence)
        if not tag: tag = 'primer'
        create_wait_html(sequence, tag, min_Tm, num_primers, max_length, min_length, is_num_primers, is_t7, job_id)

        try:
            t0 = time.time()
            assembly = Primer_Assembly(sequence, min_Tm, num_primers, min_length, max_length, tag)
            t_total = time.time() - t0
        except:
            print "\033[41mError(s)\033[0m encountered: \033[94m", sys.exc_info()[0], "\033[0m"
            print traceback.format_exc()
            create_err_html(sequence, tag, min_Tm, num_primers, max_length, min_length, is_num_primers, is_t7, job_id)
            raise cherrypy.HTTPRedirect('result?job_id=%s' % job_id)

        # time.sleep(15)

        # when no solution found
        if (not assembly.is_solution):
            msg = '<br/><hr/><div class="container theme-showcase"><div class="row"><div class="col-md-8"><h2>Output Result:</h2></div><div class="col-md-4"><h4 class="text-right"><span class="glyphicon glyphicon-search"></span>&nbsp;&nbsp;<span class="label label-violet">JOB_ID</span>: <span class="label label-inverse">__JOB_ID___</span></h4><a href="__FILE_NAME__" class="btn btn-blue pull-right" style="color: #ffffff;" title="Output in plain text" download disabled>&nbsp;Save Result&nbsp;</a></div></div><br/><div class="alert alert-danger"><p><span class="glyphicon glyphicon-minus-sign"></span>&nbsp;&nbsp;<b>FAILURE</b>: No solution found (Primerize run finished without errors).<br/><ul><li>Please examine the advanced options. Possible solutions might be restricted by stringent options combination, especially by minimum Tm and # number of primers. Try again with relaxed the advanced options.</li><li>Certain input sequence, e.g. polyA or large repeats, might be intrinsically difficult for PCR assembly design.</li><li>For further information, please feel free to <a class="btn btn-warning btn-sm path_about" href="#contact" style="color: #ffffff;">Contact</a> us to track down the problem.</li></ul></p></div>'
            msg = msg.replace('__JOB_ID___', job_id).replace('__FILE_NAME__', '/cache/result_%s.txt' % job_id)
            html_content = html_content.replace('__RESULT__', msg)
            create_res_html(html_content, job_id)
            raise cherrypy.HTTPRedirect('result?job_id=%s' % job_id)
        
        try:
            script = ''
            if len(assembly.warnings):
                script += '<br/><hr/><div class="container theme-showcase"><div class="row"><div class="col-md-8"><h2>Output Result:</h2></div><div class="col-md-4"><h4 class="text-right"><span class="glyphicon glyphicon-search"></span>&nbsp;&nbsp;<span class="label label-violet">JOB_ID</span>: <span class="label label-inverse">__JOB_ID___</span></h4><a href="__FILE_NAME__" class="btn btn-blue pull-right" style="color: #ffffff;" title="Output in plain text" download>&nbsp;Save Result&nbsp;</a></div></div><br/><div class="alert alert-warning" title="Mispriming alerts"><p>'
                for i in xrange(len(assembly.warnings)):
                    warning = assembly.warnings[i]
                    p_1 = '<b>%d</b>%s' % (warning[0], primer_suffix_html(warning[0] - 1))
                    p_2 = ', '.join('<b>%d</b>%s' % (x, primer_suffix_html(x - 1)) for x in warning[3])
                    script += '<span class="glyphicon glyphicon-exclamation-sign"></span>&nbsp;&nbsp;<b>WARNING</b>: Primer %s can misprime with <span class="label label-default">%d</span>-residue overlap to position <span class="label label-success">%s</span>, which is covered by primers: %s.<br/>' % (p_1, warning[1], str(int(warning[2])), p_2)
                script += '<span class="glyphicon glyphicon-info-sign"></span>&nbsp;&nbsp;<b>WARNING</b>: One-pot PCR assembly may fail due to mispriming; consider first assembling fragments in a preliminary PCR round (subpool).<br/>'
            else:
                script += '<div class="container theme-showcase"><div class="row"><div class="col-md-8"><h2>Output Result:</h2></div><div class="col-md-4"><h4 class="text-right"><span class="label label-violet">JOB_ID</span>: <span class="label label-inverse">__JOB_ID___</span></h4><a href="__FILE_NAME__" class="btn btn-blue pull-right" title="Output in plain text" download>&nbsp;Download&nbsp;</a></div></div><br/><div class="alert alert-success" title="No alerts"><p>'
                script += '<span class="glyphicon glyphicon-ok-sign"></span>&nbsp;&nbsp;<b>SUCCESS</b>: No potential mis-priming found. See results below.<br/>'

            script += '</p></div><div class="row"><div class="col-md-10"><div class="alert alert-default"><p>__NOTE_T7__</p></div></div><div class="col-md-2"><div class="alert alert-orange text-center"> <span class="glyphicon glyphicon-time"></span>&nbsp;&nbsp;<b>Time elapsed</b>:<br/><i>%.1f</i> s.</div></div></div>' % t_total

            script += '<div class="row"><div class="col-md-12"><div class="panel panel-primary"><div class="panel-heading"><h2 class="panel-title"><span class="glyphicon glyphicon-indent-left"></span>&nbsp;&nbsp;Designed Primers</h2></div><div class="panel-body"><table class="table table-striped table-hover" ><thead><tr><th class="col-md-1">#</th><th class="col-md-1">Length</th><th class="col-md-10">Sequence</th></tr></thead><tbody>'
            for i in xrange(len(assembly.primer_set)):
                script += '<tr><td><b>%d%s</b></td><td><em>%d</td><td style="word-break: break-all;">%s</td></tr>' % (i + 1, primer_suffix_html(i), len(assembly.primer_set[i]), assembly.primer_set[i])

            script += '</tbody></table></div></div></div></div><div class="row"><div class="col-md-12"><div class="panel panel-green"><div class="panel-heading"><h2 class="panel-title"><span class="glyphicon glyphicon-tasks"></span>&nbsp;&nbsp;Assembly Scheme</h2></div><div class="panel-body"><pre>'

            x = 0
            for line in assembly.print_lines:
                if line[0] == '~':
                    script += '<br/><span class="label-white label-primary">' + line[1] + '</span>'
                elif line[0] == '=':
                    script += '<span class="label-warning">' + line[1] + '</span>'
                elif line[0] == '^':
                    for char in line[1]:
                        if char in SEQ['valid']:
                            script += '<span class="label-info">' + char + '</span>'
                        else:
                            if char.isdigit():
                                script += '<b>' + char + '</b>'
                            elif char in ('-', '<', '>'):
                                script += '<span class="label-white label-orange">' + char + '</span>'
                            else:
                                script += char
                elif line[0] == "!":
                    for char in line[1]:
                        if char in SEQ['valid']:
                            script += '<span class="label-white label-danger">' + char + '</span>'
                        else:
                            if char.isdigit():
                                script += '<b>' + char + '</b>'
                            elif char in ('-', '<', '>'):
                                script += '<span class="label-green">' + char + '</span>'
                            else:
                                script += char
                elif (line[0] == '$'):
                    if line[1].find('xxxx') != -1: 
                        Tm = '%2.1f' % assembly.Tm_overlaps[x]
                        x += 1
                        script += line[1].replace('x' * len(Tm), '<kbd>%s</kbd>' % Tm)
                    elif '|' in line[1]:
                        script += line[1]
                script += '<br/>'

            script += '</pre></div></div></div></div><p class="lead"><span class="glyphicon glyphicon-question-sign"></span>&nbsp;&nbsp;<b><u><i>What next?</i></u></b> Try our suggested experimental <a class="btn btn-info btn-sm path_protocol" href="" role="button" style="color: #ffffff;">&nbsp;&nbsp;Protocol&nbsp;&nbsp;</a> for PCR assembly.</p> </div>'

            # f = tempfile.NamedTemporaryFile(mode="w+b", prefix="result_", suffix=".txt", dir="cache", delete=False)
            # job_id = binascii.b2a_hex(os.urandom(7)) #f.name[-17:]
            file_name = 'cache/result_%s.txt' % job_id
            f = open(file_name, 'w')

            f.write('Primerize Result\n\nINPUT\n=====\n%s\n' % sequence)
            f.write('#\nMIN_TM: %.1f\n' % min_Tm)
            if num_primers == ARG['DEF_NUM_PRM']:
                f.write('NUM_PRIMERS: auto (unspecified)')
            else:
                f.write('NUM_PRIMERS: %d' % num_primers)
            f.write('\nMAX_LENGTH: %d\nMIN_LENGTH: %d\n' % (max_length, min_length))
            if '1' in is_t7:
                str_t7 = '<span class="glyphicon glyphicon-plus-sign"></span>&nbsp;&nbsp;T7_CHECK: feature enabled (uncheck the option to disable). T7 promoter sequence '
                if flag:
                    str_t7 = str_t7 + 'is present, no action was taken.\n'
                else:
                    str_t7 = str_t7 + 'was absent, Primerize automatically prepended it. \n'
                if is_G:
                    str_t7 += '<span class="glyphicon glyphicon-ok-sign"></span>&nbsp;&nbsp;SUCCESS: T7 promoter sequence is followed by nucleotides GG.\n'
                else:
                    str_t7 += '<span class="glyphicon glyphicon-exclamation-sign"></span>&nbsp;&nbsp;WARNING: T7 promoter sequence is NOT followed by nucleotides GG. Consider modifying the sequence for better transcription.\n'
            else:
                str_t7 = 'T7_CHECK: feature disabled (check the option to enable). No checking was performed.\n'
            f.write(str_t7.replace('SUCCESS', 'T7_CHECK').replace('WARNING', 'T7_CHECK').replace('<span class="glyphicon glyphicon-ok-sign"></span>&nbsp;&nbsp;', '').replace('<span class="glyphicon glyphicon-plus-sign"></span>&nbsp;&nbsp;', '').replace('<span class="glyphicon glyphicon-exclamation-sign"></span>&nbsp;&nbsp;', ''))
            script = script.replace('__NOTE_T7__', str_t7.replace('\n', '<br/>').replace('T7_CHECK', '<b>T7_CHECK</b>').replace('SUCCESS', '<b>SUCCESS</b>').replace('WARNING', '<b>WARNING</b>').replace('NOT', '<u><b>NOT</b></u>').replace('nucleotides GG', 'nucleotides <u>GG</u>'))

            f.write('\n\nOUTPUT\n======\n')
            lines = assembly.print_assembly() + assembly.print_primers() + assembly.print_warnings()
            lines = lines.replace('\033[0m', '').replace('\033[100m', '').replace('\033[92m', '').replace('\033[93m', '').replace('\033[94m', '').replace('\033[95m', '').replace('\033[96m', '').replace('\033[41m', '')
            f.write(lines)
            f.write('#\n\n------/* IDT USER: for primer ordering, copy and paste to Bulk Input */------\n------/* START */------\n')
            for i in xrange(len(assembly.primer_set)):
                if i % 2:
                    suffix = 'R'
                else:
                    suffix = 'F'
                f.write('%s-%d%s\t%s\t\t25nm\tSTD\n' % (tag, i + 1, suffix, assembly.primer_set[i]))
            f.write('------/* END */------\n------/* NOTE: use "Lab Ready" for "Normalization" */------\n')

            script = script.replace('__FILE_NAME__', '/' + file_name).replace('__JOB_ID___', job_id)
            f.close()

            html_content = get_first_part_of_page(sequence, tag, min_Tm, num_primers, max_length, min_length, is_num_primers, is_t7).replace('__RESULT__', script)
            create_res_html(html_content, job_id)
        except:
            print "\033[41mError(s)\033[0m encountered: \033[94m", sys.exc_info()[0], "\033[0m"
            print traceback.format_exc()
            create_err_html(sequence, tag, min_Tm, num_primers, max_length, min_length, is_num_primers, is_t7, job_id)

    raise cherrypy.HTTPRedirect('result?job_id=%s' % job_id)


