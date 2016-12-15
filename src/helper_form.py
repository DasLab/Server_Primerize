from django.http import HttpResponse

import re
import string

from src.helper import *
from src.settings import *


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
        if not is_valid_name(char, "-", 1): return 0
    return 1

# def is_valid_sequence(sequence):
#     for e in sequence.upper():
#         if e in SEQ['valid']:
#             return 1
#     return 0

def is_t7_present(sequence):
    if sequence.startswith(SEQ['T7']):
        is_G = sequence[20:].startswith('GG')
        return (sequence, 1, is_G)
    else:
        is_G = sequence.startswith('GG')
        return (SEQ['T7'] + sequence, 0, is_G)


def form_data_clean_common(form_data):
    sequence = form_data['sequence']
    sequence = re.sub('[^' + ''.join(SEQ['valid']) + ']', '', sequence.upper().replace('U', 'T')).encode('utf-8', 'ignore')
    tag = form_data['tag']
    tag = re.sub('[^a-zA-Z0-9\ \.\-\_]', '', tag)
    if not tag: tag = 'primer'
    return (sequence, tag)

def form_data_clean_primers(primers):
    primers = re.sub('[^' + ''.join(SEQ['valid']) + ''.join(SEQ['valid']).lower() + '\ \,]', '', primers)
    primers = [str(p.strip()) for p in primers.split(',') if p.strip()]
    return primers

def form_data_clean_structures(structures):
    structures = re.sub('[^' + '\\'.join(STR['valid']) + '\ \,]', '', structures)
    structures = [str(s.strip()) for s in structures.split(',') if s.strip()]
    return structures

def form_data_clean_1d(form_data, sequence):
    min_Tm = form_data['min_Tm']
    max_len = form_data['max_len']
    min_len = form_data['min_len']
    num_primers = form_data['num_primers']
    is_num_primers = form_data['is_num_primers']
    is_check_t7 = form_data['is_check_t7']
    if not min_Tm: min_Tm = ARG['MIN_TM']
    if not max_len: max_len = ARG['MAX_LEN']
    if not min_len: min_len = ARG['MIN_LEN']
    if len(sequence) > 500: min_len = max(30, min_len)
    if (not num_primers) or (not is_num_primers): num_primers = ARG['NUM_PRM']
    return (min_Tm, max_len, min_len, num_primers, is_num_primers, is_check_t7)

def form_clean_data_2d(form_data, sequence):
    primers = form_data_clean_primers(form_data['primers'])
    offset = form_data['offset']
    min_muts = form_data['min_muts']
    max_muts = form_data['max_muts']
    lib = form_data['lib']
    if not offset: offset = 0
    (which_muts, min_muts, max_muts) = primerize.util.get_mut_range(min_muts, max_muts, offset, sequence)
    if not lib: lib = '1'
    which_lib = [int(lib)]
    return (primers, offset, min_muts, max_muts, which_muts, which_lib)

def form_clean_data_3d(form_data, sequence):
    (primers, offset, min_muts, max_muts, which_muts, which_lib) = form_clean_data_2d(form_data, sequence)
    structures = form_data_clean_structures(form_data['structures'])
    is_single = form_data['is_single']
    is_fill_WT = form_data['is_fill_WT']
    num_mutations = form_data['num_mutations']
    if not num_mutations: num_mutations = '1'
    num_mutations = int(num_mutations)
    return (primers, offset, min_muts, max_muts, which_muts, which_lib, structures, is_single, is_fill_WT, num_mutations)


def form_check_valid(type, sequence, num_primers=0, primers=[], min_muts=None, max_muts=None, structures=[]):
    if len(sequence) < 60:
        return HttpResponse(simplejson.dumps({'error': '10', 'type': type}, sort_keys=True, indent=' ' * 4), content_type='application/json')
    elif len(sequence) > 1000:
        return HttpResponse(simplejson.dumps({'error': '11', 'type': type}, sort_keys=True, indent=' ' * 4), content_type='application/json')
    elif num_primers % 2:
        return HttpResponse(simplejson.dumps({'error': '20', 'type': type}, sort_keys=True, indent=' ' * 4), content_type='application/json')

    if type >= 2:
        if type == 3:
            if not structures:
                return HttpResponse(simplejson.dumps({'error': '40', 'type': type}, sort_keys=True, indent=' ' * 4), content_type='application/json')
            len_str = map(len, structures)
            len_str = all([s == len(sequence) for s in len_str])
            if not len_str:
                return HttpResponse(simplejson.dumps({'error': '41', 'type': type}, sort_keys=True, indent=' ' * 4), content_type='application/json')

        if len(primers) % 2:
            return HttpResponse(simplejson.dumps({'error': '21', 'type': type}, sort_keys=True, indent=' ' * 4), content_type='application/json')
        elif min_muts > max_muts:
            return HttpResponse(simplejson.dumps({'error': '30', 'type': type}, sort_keys=True, indent=' ' * 4), content_type='application/json')

        if not primers:
            assembly = prm_1d.design(sequence)
            if assembly.is_success:
                primers = assembly.primer_set
            else:
                return HttpResponse(simplejson.dumps({'error': '01', 'type': type}, sort_keys=True, indent=' ' * 4), content_type='application/json')
    return (None, primers)
