import os
import string

from const import *

MEDIA_DIR = os.path.join(os.path.abspath("."))


def load_html(file_name):
    f = open(file_name, "r")
    lines = f.readlines()
    f.close()
    script = "".join(lines)
    return script


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
    script = load_html(PATH_DESIGN)
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

    if num_primers in (str(DEF_NUM_PRM), " ","auto"): num_primers = "auto"
    script = script.replace("__SEQ__", sequence).replace("__MIN_TM__", min_Tm).replace("__NUM_PRIMERS__", num_primers).replace("__MAX_LEN__", max_length).replace("__MIN_LEN__", min_length).replace("__TAG__", tag).replace("__LEN__", str(len(sequence))).replace("__IS_NUM_PRMS__", is_num_primers).replace("__IS_NUM_PRMS_DIS__", is_num_primers_disabled)
    return script


def is_valid_sequence(sequence):
	res = "A,G,C,U,T".split(",")
	for e in sequence.upper():
		if e not in res:
			return 0
	return 1
