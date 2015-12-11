import os
import xlwt

from thermo import *


def DNA2RNA(sequence):
    return sequence.upper().replace('T', 'U')


def RNA2DNA(sequence):
    return sequence.upper().replace('U', 'T')


def complement(sequence):
    sequence = list(sequence)
    rc_dict = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
    for i in range(len(sequence)):
        sequence[i] = rc_dict[sequence[i]]
    return ''.join(sequence)


def reverse_complement(sequence):
    sequence = sequence[::-1]
    return complement(sequence)


def primer_suffix(num):
    if num % 2:
        return '\033[95m R\033[0m'
    else:
        return '\033[94m F\033[0m'


def draw_assembly(sequence, primers, name, COL_SIZE=142):
    N_primers = primers.shape[1]
    seq_line_prev = list(' ' * max(len(sequence), COL_SIZE))
    bp_lines = []
    seq_lines = []
    Tms = []

    for i in xrange(N_primers):
        primer = primers[:, i]
        seq_line = list(' ' * max(len(sequence), COL_SIZE))
        (seg_start, seg_end, seg_dir) = primer

        if (seg_dir == 1):
            for j in xrange(seg_start, seg_end + 1):
                seq_line[j] = sequence[j]

            if (seg_end + 1 < len(sequence)):
                seq_line[seg_end + 1] = '-'
            if (seg_end + 2 < len(sequence)):
                seq_line[seg_end + 2] = '>'

            num_txt = '%d' % (i + 1)
            if (seg_end + 4 + len(num_txt) < len(sequence)):
                offset = seg_end + 4
                seq_line[offset:(offset + len(num_txt))] = num_txt
        else:
            for j in xrange(seg_start, seg_end + 1):
                seq_line[j] = reverse_complement(sequence[j])

            if (seg_start - 1 >= 0):
                seq_line[seg_start - 1] = '-'
            if (seg_start - 2 >= 0):
                seq_line[seg_start - 2] = '<'

            num_txt = '%d' % (i + 1)
            if (seg_start - 3 - len(num_txt) >= 0):
                offset = seg_start - 3 - len(num_txt)
                seq_line[offset:(offset + len(num_txt))] = num_txt

        bp_line = list(' ' * max(len(sequence), COL_SIZE))
        overlap_seq = ''
        last_bp_pos = 1
        for j in xrange(len(sequence)):
            if (seq_line_prev[j] in 'ACGT' and seq_line[j] in 'ACGT'):
                bp_line[j] = '|'
                last_bp_pos = j
                overlap_seq += sequence[j]

        if (last_bp_pos > 1):
            Tm = calc_Tm(overlap_seq, 0.2e-6, 0.1, 0.0015)
            Tms.append(Tm)
            Tm_txt = '%2.1f' % Tm
            offset = last_bp_pos + 2
            bp_line[offset:(offset + len(Tm_txt))] = 'x' * len(Tm_txt)

        bp_lines.append(''.join(bp_line))
        seq_lines.append(''.join(seq_line))
        seq_line_prev = seq_line

    print_lines = []
    for i in xrange(int(math.floor((len(sequence) - 1) / COL_SIZE)) + 1):
        start_pos = COL_SIZE * i
        end_pos = min(COL_SIZE * (i + 1), len(sequence))
        out_line = sequence[start_pos:end_pos]
        print_lines.append(('~', out_line))

        for j in xrange(len(seq_lines)):
            if (len(bp_lines[j][end_pos:].replace(' ', '')) and ('|' not in bp_lines[j][end_pos:].replace(' ', '')) and (not len(bp_lines[j][:start_pos].replace(' ', '')))):
                bp_line = bp_lines[j][start_pos:].rstrip()
            elif ('|' not in bp_lines[j][start_pos:end_pos]):
                bp_line = ' ' * (end_pos - start_pos + 1)
            else:
                bp_line = bp_lines[j][start_pos:end_pos]
            seq_line = seq_lines[j][start_pos:end_pos]

            if len(bp_line.replace(' ', '')) or len(seq_line.replace(' ', '')):
                print_lines.append(('$', bp_line))
                if j % 2:
                    print_lines.append(('!', seq_line))
                else:
                    print_lines.append(('^', seq_line))
        print_lines.append(('$', ' ' * (end_pos - start_pos + 1)))
        print_lines.append(('=', complement(out_line)))
        print_lines.append(('', '\n'))

    return (bp_lines, seq_lines, print_lines, Tms)


def coord_to_num(coord):
    coord = coord.upper().strip()
    row = 'ABCDEFGH'.find(coord[0])
    if row == -1: return -1
    col = int(coord[1:])
    if col < 0 or col > 12: return -1
    return (col - 1) * 8 + row + 1


def num_to_coord(num):
    if num < 0 or num > 96: return -1
    row = 'ABCDEFGH'[(num - 1) % 8]
    col = (num - 1) / 8 + 1
    return '%s%d' % (row, col)


def get_primer_index(primer_set, sequence):
    N_primers = len(primer_set)
    primers = numpy.zeros((3, N_primers))

    for n in xrange(N_primers):
        primer = RNA2DNA(primer_set[n])
        if n % 2:
            i = sequence.find(reverse_complement(primer))
        else:
            i = sequence.find(primer)
        if i == -1:
            return ([], True)
        else:
            start_pos = i
            end_pos = i + len(primer_set[n]) - 1
            seq_dir = math.copysign(1, 0.5 - n % 2)
            primers[:, n] = [start_pos, end_pos, seq_dir]

    return (primers.astype(int), False)


def get_mutation(nt, lib):
    idx = 'ATCG'.find(nt)
    if lib == 1:
        return 'TAGC'[idx]
    elif lib == 2:
        return 'CCAA'[idx]
    elif lib == 3:
        return 'GGTT'[idx]


def print_primer_plate(plate, ref_primer):
    string = ''
    for key in sorted(plate.data):
        string += '\033[94m%s\033[0m' % num_to_coord(key).ljust(5)
        mut = plate.data[key][0]
        if mut[-2:] == 'WT':
            string += ('%s\033[100m%s\033[0m' % (mut[:-2], mut[-2:])).ljust(28)
        else:
            string += ('%s\033[96m%s\033[0m\033[93m%s\033[0m\033[91m%s\033[0m' % (mut[:5], mut[5], mut[6:-1], mut[-1])).ljust(45)

        if ref_primer:
            for i in xrange(len(ref_primer)):
                if ref_primer[i] != plate.data[key][1][i]:
                    string += '\033[41m%s\033[0m' % plate.data[key][1][i]
                else:
                    string += plate.data[key][1][i]

        else:
            string += plate.data[key][1]
        string += '\n'

    if not string: string = '(empty)\n'
    return string


def save_construct_key(keys, prefix, path):
    f = open(os.path.join(path, '%s_keys.txt' % prefix), 'w')
    print 'Creating keys file ...'
    f.write('\n'.join(keys))
    f.close()


def save_plates_excel(plates, N_plates, N_primers, prefix, path):
    for k in xrange(N_plates):
        file_name = os.path.join(path, '%s_plate_%d.xls' % (prefix, k + 1))
        print 'Creating plate file: \033[94m%s\033[0m.' % file_name
        workbook = xlwt.Workbook()

        for p in xrange(N_primers):
            primer_sequences = plates[p][k]
            num_primers_on_plate = primer_sequences.get_count()

            if num_primers_on_plate:
                sheet = workbook.add_sheet('primer_%d' % (p + 1))
                sheet.col(1).width = 256 * 15
                sheet.col(2).width = 256 * 75

                sheet.write(0, 0, 'WellPosition', xlwt.easyxf('font: bold 1'))
                sheet.write(0, 1, 'Name', xlwt.easyxf('font: bold 1'))
                sheet.write(0, 2, 'Sequence', xlwt.easyxf('font: bold 1'))
                sheet.write(0, 3, 'Notes', xlwt.easyxf('font: bold 1'))

                for i, row in enumerate(sorted(primer_sequences.data)):
                    if 'WT' in primer_sequences.data[row][0]:
                        sheet.write(i + 1, 0, num_to_coord(row), xlwt.easyxf('font: color blue, italic 1'))
                        sheet.write(i + 1, 1, primer_sequences.data[row][0], xlwt.easyxf('font: color blue'))
                        sheet.write(i + 1, 2, primer_sequences.data[row][1], xlwt.easyxf('font: color blue'))
                    else:
                        sheet.write(i + 1, 0, num_to_coord(row), xlwt.easyxf('font: italic 1'))
                        sheet.write(i + 1, 1, primer_sequences.data[row][0])
                        sheet.write(i + 1, 2, primer_sequences.data[row][1])

        workbook.save(file_name)    

