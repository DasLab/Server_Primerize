from src.settings import *
from src.models import *
from src.helper import *


def create_HTML_page_result(html_content, job_id, type):
    open(MEDIA_ROOT + '/data/%dd/result_%s.html' % (type, job_id), 'w').write(html_content.encode('utf-8', 'ignore'))

def create_HTML_page_wait(job_id, type):
    html = '<br/><hr/><div class="row"><div class="col-lg-12 col-md-12 col-sm-12 col-xs-12"><h2><span class="glyphicon glyphicon-hourglass"></span>&nbsp;&nbsp;Primerize is running...  </h2></div></div><br/><div class="progress"><div class="progress-bar progress-bar-striped active" role="progressbar" aria-valuenow="100" aria-valuemin="0" aria-valuemax="100" style="width: 100%%;"><span class="sr-only"></span></div></div><h3 class="text-center">Your <span class="label label-violet">JOB_ID</span> is: <span class="label label-inverse">%s</span></h3><br/><br/><img class="center-block" src="/site_media/images/fg_loader.gif" width="48px" style="opacity:0.5;"/><br/><br/><div class="row"><div class="col-lg-6 col-md-6 col-sm-7 col-xs-7"><p>Your query is being processed. Usually, the calculation is finished within 30 seconds. Depending on the input sequence length and complexity, the run may take longer.</p><p>You can close the browser and retrieve the result later using the above unique <span class="label label-violet">JOB_ID</span>. The cached result expires after 9 months.</p></div><div class="col-lg-6 col-md-6 col-sm-5 col-xs-5"><p class="text-center well" ><b>Please <button id="btn-copy" class="btn btn-success" data-clipboard-target="#url_id"><span class="glyphicon glyphicon-copy"></span>&nbsp;&nbsp;Copy&nbsp;</button> this link: <br/><code id="url_id" style="word-wrap:break-word;">http://primerize.stanford.edu/result/?job_id=%s</code></b></p><br/></div><script type="text/javascript">var client = new Clipboard("#btn-copy");</script>' % (job_id, job_id)
    create_HTML_page_result(html, job_id, type)

def create_HTML_page_error(job_id, t_total, type):
    html = '<br/><hr/><div class="row"><div class="col-lg-8 col-md-8 col-sm-6 col-xs-6"><h2><span class="glyphicon glyphicon-ban-circle"></span>&nbsp;&nbsp;Primerize has difficulty in your query...</h2></div><div class="col-lg-4 col-md-4 col-sm-6 col-xs-6"><h4 class="text-right"><span class="glyphicon glyphicon-search"></span>&nbsp;&nbsp;<span class="label label-violet">JOB_ID</span>: <span class="label label-inverse">%s</span></h4><button class="btn btn-blue pull-right" style="color: #ffffff;" title="Output in plain text" disabled><span class="glyphicon glyphicon-download-alt"></span>&nbsp;&nbsp;Save Result&nbsp;</button></div></div><br/><div class="progress"><div class="progress-bar progress-bar-danger progress-bar-striped" role="progressbar" aria-valuenow="100" aria-valuemin="0" aria-valuemax="100" style="width: 100%%"><span class="sr-only"></span></div></div><br/><p>Primerize encountered an internal error while processing your query. Sorry for the inconvenience. </p><p>We will investigate and fix the problem.</p><p>For further information, please feel free to <a class="btn btn-warning btn-sm" href="/about/#contact" style="color: #ffffff;"><span class="glyphicon glyphicon-send"></span>&nbsp;&nbsp;Contact&nbsp;</a> us to track down the problem.</p>' % (job_id)
    if type == 1:
        job_entry = Design1D.objects.get(job_id=job_id)
    elif type == 2:
        job_entry = Design2D.objects.get(job_id=job_id)
    elif type == 3:
        job_entry = Design3D.objects.get(job_id=job_id)
    job_entry.status = '4'
    job_entry.time = t_total
    job_entry.save()

    script_500 = ''.join(open(PATH.HTML_PATH['500'], 'r').readlines())
    script_500 = script_500[script_500.find('<div class="row bgimg2-lg'):script_500.find('endblock') - 3]
    create_HTML_page_result(html + script_500, job_id, type)

def create_HTML_page_fail(job_id, type):
    html = HTML_elem_header(job_id, True, type)
    html += '<div class="alert alert-danger"><p><span class="glyphicon glyphicon-minus-sign"></span>&nbsp;&nbsp;<b>FAILURE</b>: No solution found (Primerize run finished without errors).<br/><ul><li>'
    if type == 1:
        html += 'Please examine the advanced options. Possible solutions might be restricted by stringent options combination, especially by minimum Tm and # number of primers. Try again with relaxed the advanced options.</li><li>Certain input sequence, e.g. polyA or large repeats, might be intrinsically difficult for PCR assembly design.'
    else:
        html += 'Please examine the primers input. Make sure the primer sequences and their order are correct, and their assembly match the full sequence. Try again with the correct input.'
    html += '</li><li>For further information, please feel free to <a class="btn btn-warning btn-sm" href="/about/#contact" style="color: #ffffff;"><span class="glyphicon glyphicon-send"></span>&nbsp;&nbsp;Contact&nbsp;</a> us to track down the problem.</li></ul></p></div>'

    job_entry = []
    if type == 1 and job_id != ARG['DEMO_1D_ID']:
        job_entry = Design1D.objects.get(job_id=job_id)
    elif type == 2 and ARG['DEMO_2D_ID']:
        job_entry = Design2D.objects.get(job_id=job_id)
    elif type == 3 and job_id not in (ARG['DEMO_3D_ID_1'], ARG['DEMO_3D_ID_2']):
        job_entry = Design3D.objects.get(job_id=job_id)
    if job_entry:
        job_entry.status = '3'
        job_entry.save()
    return create_HTML_page_result(html, job_id, type)


def HTML_elem_primer_suffix(num):
    return '<span class="label label-danger">R</span>' if num % 2 else '<span class="label label-info">F</span>'

def HTML_elem_header(job_id, disabled, type):
    url = '/site_data/1d/result_%s.txt' % job_id if type == 1 else '/site_data/%dd/result_%s.zip' % (type, job_id)
    elem = 'button' if disabled else 'a'
    action = 'disabled' if disabled else 'download'
    url = '' if disabled else 'href="%s"' % url

    return '<br/><hr/><div class="row"><div class="col-lg-8 col-md-8 col-sm-6 col-xs-6"><h2>Output Result:</h2></div><div class="col-lg-4 col-md-4 col-sm-6 col-xs-6"><h4 class="text-right"><span class="glyphicon glyphicon-search"></span>&nbsp;&nbsp;<span class="label label-violet">JOB_ID</span>: <span class="label label-inverse">%s</span></h4><%s %s class="btn btn-blue pull-right" style="color: #ffffff;" title="Output in plain text" %s><span class="glyphicon glyphicon-download-alt"></span>&nbsp;&nbsp;Save Result&nbsp;</%s></div></div><br/>' % (job_id, elem, url, action, elem)

def HTML_elem_time_elapsed(t_total, type):
    alert = 'default' if type == 1 else 'warning'
    placeholder = '__NOTE_T7__' if type == 1 else '__NOTE_NUM__'
    return '<div class="row equal"><div class="col-lg-10 col-md-10 col-sm-9 col-xs-9"><div class="alert alert-%s"><p>%s</p></div></div><div class="col-lg-2 col-md-2 col-sm-3 col-xs-3"><div class="alert alert-orange text-center"> <span class="glyphicon glyphicon-time"></span>&nbsp;&nbsp;<b>Time elapsed</b>:<br/><i>%.1f</i> s.</div></div></div>' % (alert, placeholder, t_total)

def HTML_elem_whats_next():
    return '<p class="lead"><span class="glyphicon glyphicon-question-sign"></span>&nbsp;&nbsp;<b><u><i>What\'s next?</i></u></b> Try our suggested experimental <a id="btn-result-to-protocol" class="btn btn-info btn-sm btn-spa" href="/protocol/#par_prep" role="button" style="color: #ffffff;"><span class="glyphicon glyphicon-file"></span>&nbsp;&nbsp;Protocol&nbsp;</a>'


def HTML_comp_assembly(illustration):
    script = illustration.replace('->', '<span class="label-white label-orange glyphicon glyphicon-arrow-right" style="margin-left:2px; padding-left:1px;"></span>').replace('<-', '<span class="label-white label-green glyphicon glyphicon-arrow-left" style="margin-right:2px; padding-right:1px;"></span>').replace('\033[92m', '<span class="label-white label-primary">').replace('\033[96m', '<span class="label-warning">').replace('\033[94m', '<span class="label-info">').replace('\033[95m', '<span class="label-white label-danger">').replace('\033[41m', '<span class="label-white label-inverse">').replace('\033[100m', '<span style="font-weight:bold;">').replace('\033[0m', '</span>').replace('\n', '<br/>')
    script = '<div class="row"><div class="col-lg-12 col-md-12 col-sm-12 col-xs-12"><div class="panel panel-green"><div class="panel-heading"><h2 class="panel-title"><span class="glyphicon glyphicon-tasks"></span>&nbsp;&nbsp;Assembly Scheme</h2></div><div class="panel-body"><pre style="font-size:12px;">%s</pre></div></div></div></div>' % script
    return script

def HTML_comp_primers(assembly):
    script = '<div class="row"><div class="col-lg-12 col-md-12 col-sm-12 col-xs-12"><div class="panel panel-primary"><div class="panel-heading"><h2 class="panel-title"><span class="glyphicon glyphicon-indent-left"></span>&nbsp;&nbsp;Designed Primers</h2></div><div class="panel-body"><table class="table table-striped table-hover" ><thead><tr class="active"><th class="col-lg-1 col-md-1 col-sm-1 col-xs-1">#</th><th class="col-lg-1 col-md-1 col-sm-1 col-xs-1">Length</th><th class="col-lg-10 col-md-10 col-sm-10 col-xs-10">Sequence</th></tr></thead><tbody>'
    for i, primer in enumerate(assembly.primer_set):
        script += '<tr><td><b>%d</b> %s</td><td><em>%d</em></td><td style="word-break:break-all" class="monospace">%s</td></tr>' % (i + 1, HTML_elem_primer_suffix(i), len(primer), primer)

    script += '<tr><td colspan="3" style="padding: 0px;"></td></tr></tbody></table></div></div></div></div>'
    return script

def HTML_comp_warnings(flag, script, type):
    if type == 1:
        warnings = flag.get('WARNING')
        if len(warnings):
            for w in warnings:
                p_1 = '<b>%d</b> %s' % (w[0], HTML_elem_primer_suffix(w[0] - 1))
                p_2 = ', '.join('<b>%d</b> %s' % (x, HTML_elem_primer_suffix(x - 1)) for x in w[3])
                script += '<span class="glyphicon glyphicon-exclamation-sign"></span>&nbsp;&nbsp;<b>WARNING</b>: Primer %s can misprime with <span class="label label-default">%d</span>-residue overlap to position <span class="label label-success">%s</span>, which is covered by primers: %s.<br/>' % (p_1, w[1], str(int(w[2])), p_2)
            script += '<span class="glyphicon glyphicon-info-sign"></span>&nbsp;&nbsp;<b>WARNING</b>: One-pot PCR assembly may fail due to mispriming; consider first assembling fragments in a preliminary PCR round (subpool).<br/>'
        else:
            script += '<span class="glyphicon glyphicon-ok-sign"></span>&nbsp;&nbsp;<b>SUCCESS</b>: No potential mis-priming found. See results below.<br/>'
            script = script.replace('alert-warning', 'alert-success')
        return script
    else:
        if flag:
            warning = ''
            for key in flag.keys():
                if len(flag[key]):
                    warning += '<span class="glyphicon glyphicon-exclamation-sign"></span>&nbsp;&nbsp;<b>WARNING</b>: <i>Plate</i> #<span class="label label-orange">%d</span> ' % key
                    for f in flag[key]:
                        warning += '<i>Primer</i> <b>%d</b> %s, ' % (f[0], HTML_elem_primer_suffix(f[0] - 1))
                    warning = warning[:-2]
                    warning += ' have fewer than <u>24</u> wells filled.<br/>'
            warning += '<span class="glyphicon glyphicon-info-sign"></span>&nbsp;&nbsp;<b>WARNING</b>: Group multiple plates that have fewer than <u>24</u> wells together before ordering.<br/>'
            return script.replace('__NOTE_NUM__', warning)
        else:
            return script.replace('<div class="alert alert-warning"><p>__NOTE_NUM__</p></div>', '<div class="alert alert-success"><p><span class="glyphicon glyphicon-ok-sign"></span>&nbsp;&nbsp;<b>SUCCESS</b>: All plates are ready to go. No editing is needed before placing the order.</p></div>')

def HTML_comp_t7_check(job_id, script, flag, is_t7, is_G):
    file_name = MEDIA_ROOT + '/data/1d/result_%s.txt' % job_id
    lines = ''.join(open(file_name, 'r').readlines())
    insert_where = '\n\nOUTPUT\n======\n'

    if is_t7:
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
    lines = lines.replace(insert_where, str_t7.replace('SUCCESS', 'T7_CHECK').replace('WARNING', 'T7_CHECK').replace('<span class="glyphicon glyphicon-ok-sign"></span>&nbsp;&nbsp;', '').replace('<span class="glyphicon glyphicon-plus-sign"></span>&nbsp;&nbsp;', '').replace('<span class="glyphicon glyphicon-exclamation-sign"></span>&nbsp;&nbsp;', '') + insert_where)
    open(file_name, 'w').write(lines)
    return script.replace('__NOTE_T7__', str_t7.replace('\n', '<br/>').replace('T7_CHECK', '<b>T7_CHECK</b>').replace('SUCCESS', '<b>SUCCESS</b>').replace('WARNING', '<b>WARNING</b>').replace('NOT', '<u><b>NOT</b></u>').replace('nucleotides GG', 'nucleotides <u>GG</u>'))

def HTML_comp_illustration(plate, script, type):
    if type == 2:
        (illustration_1, illustration_2, illustration_3) = plate._data['illustration']['lines']
    else:
        (illustration_3, illustration_2, illustration_1, illustration_str) = plate._data['illustration']['lines']
    illustration_1 = illustration_1.replace(' ', '&nbsp;').replace('\033[91m', '<span class="label-white label-default" style="color:#c28fdd;">').replace('\033[44m', '<span class="label-green" style="color:#ff7c55;">').replace('\033[46m', '<span class="label-green">').replace('\033[40m', '<span class="label-white label-default">').replace('\033[0m', '</span>')
    illustration_2 = illustration_2.replace(' ', '&nbsp;').replace('\033[92m', '<span style="color:#ff7c55;">').replace('\033[91m', '<span style="color:#c28fdd;">').replace('\033[0m', '</span>')
    illustration_3 = illustration_3.replace(' ', '&nbsp;').replace('\033[92m', '<span style="color:#ff7c55;">').replace('\033[91m', '<span style="color:#c28fdd;">').replace('\033[0m', '</span>')

    if type == 2:
        return script.replace('__SEQ_ANNOT__', illustration_1 + '</p><p class="text-right" style="margin-top:2px;">&nbsp;<span class="monospace">' + illustration_2 + '</p><p class="text-right" style="margin-top:0px;">&nbsp;<span class="monospace">' + illustration_3)
    else:
        illustration_str = illustration_str.replace(' ', '&nbsp;').replace('\033[43m', '<span class="label-white label-primary">').replace('\033[0m', '</span>')

        (illustration_str_annotated, illustration_1_annotated) = ('', '')
        num = 1 - plate._params['offset']
        for char in illustration_1:
            if char in ''.join(SEQ['valid']):
                illustration_1_annotated += '<span class="seqpos_%d">%s</span>' % (num, char)
                num += 1
            else:
                illustration_1_annotated += char

        for ill_str in illustration_str.split('\n'):
            num = 1 - plate._params['offset']
            for i, char in enumerate(ill_str):
                if char in ''.join(STR['valid']):
                    illustration_str_annotated += '<span class="seqpos_%d">%s</span>' % (num, char)
                    num += 1
                else:
                    illustration_str_annotated += char
            illustration_str_annotated += '<br/>'
        illustration_1 = illustration_1_annotated
        illustration_str = illustration_str_annotated[:-5] if len(plate.structures) >= 5 else illustration_str_annotated
        illustration_final = illustration_3 + '<br/>' + illustration_2 + '<br/>' + illustration_1 + '<br/><span style="white-space:pre;">' + illustration_str + '</span>'
        illustration_final = illustration_final + illustration_1 + '<br/><br/>' if len(plate.structures) >= 5 else illustration_final
        return script.replace('__SEQ_ANNOT__', illustration_final)

def HTML_comp_plates(plate, script, job_id, type):
    script += '<div class="row"><div class="col-lg-12 col-md-12 col-sm-12 col-xs-12"><div class="panel panel-primary"><div class="panel-heading"><h2 class="panel-title"><span class="glyphicon glyphicon-th"></span>&nbsp;&nbsp;Plate Layout</h2></div><div class="panel-body">'
    json = {'plates': {}}
    primer_set = plate.primer_set
    flag = {}
    for i in xrange(plate.get('N_PLATE')):
        flag[i + 1] = []
        json['plates'][i + 1] = {'primers': {}}
        construct_list = primerize.Plate_96Well()
        script += '<div class="row"><div class="col-lg-12 col-md-12 col-sm-12 col-xs-12"><p class="lead">Plate # <span class="label label-orange">%d</span> <span style="font-size:small;">(<span class="glyphicon glyphicon-stats" style="color:#b7bac5;"></span> <u>__N_CONSTRUCT_PLATE__</u>)</span></p></div></div><div class="row">' % (i + 1)

        for j in xrange(plate.get('N_PRIMER')):
            primer_sequences = plate._data['plates'][j][i]
            num_primers_on_plate = len(primer_sequences)

            if num_primers_on_plate:
                if num_primers_on_plate == 1 and 'A01' in primer_sequences:
                    tag = primer_sequences.get('A01')[0]
                    if (isinstance(tag, primerize.Mutation) and not tag) or (isinstance(tag, str) and 'WT' in tag): continue

                if num_primers_on_plate < 24:
                    flag[i + 1].append((j + 1, num_primers_on_plate))

                json['plates'][i + 1]['primers'][j + 1] = []
                script += '<div class="col-lg-3 col-md-3 col-sm-4 col-xs-6"><div class="thumbnail"><div id="svg_plt_%d_prm_%d"></div><div class="caption"><p class="text-center center-block" style="margin-bottom:0px;"><i>Primer</i> <b>%d</b> %s <span style="font-size:small;">(<span class="glyphicon glyphicon-stats" style="color:#b7bac5;"></span> <u>%s</u>)</span></p></div></div></div>' % (i + 1, j + 1, j + 1, HTML_elem_primer_suffix(j), num_primers_on_plate)

                for k in xrange(96):
                    if k + 1 in primer_sequences._data:
                        row = primer_sequences._data[k + 1]
                        if isinstance(row[0], primerize.Mutation):
                            lbl = ';'.join(row[0].list()) if row[0] else 'WT'
                            lbl = primer_sequences.tag + lbl
                        else:
                            lbl = row[0]
                        if row[1] == primer_set[j] and lbl != 'WT':
                            json['plates'][i + 1]['primers'][j + 1].append({'coord': k + 1, 'label': lbl, 'pos': primerize.util.num_to_coord(k + 1), 'sequence': row[1], 'color': 'green'})
                        else:
                            json['plates'][i + 1]['primers'][j + 1].append({'coord': k + 1, 'label': lbl, 'pos': primerize.util.num_to_coord(k + 1), 'sequence': row[1]})
                        construct_list.set(primerize.util.num_to_coord(k + 1), '', '')
                    else:
                        json['plates'][i + 1]['primers'][j + 1].append({'coord': k + 1})

        if not flag[i + 1]: del flag[i + 1]
        script += '</div>'
        script = script.replace('__N_CONSTRUCT_PLATE__', str(len(construct_list)))
    script += '</div></div></div></div></div>'

    save_plate_json(json, job_id, type)
    return (script, flag)

