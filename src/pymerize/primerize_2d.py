import math
from numba import jit
import numpy
import sys
import time

from util import *
from primerize_1d import *


class Mutate_Map(object):
    def __init__(self, sequence, primer_set, offset, which_muts, which_libs, prefix):
        self.sequence = RNA2DNA(sequence)

        self.primer_set = primer_set
        self.offset = offset
        self.which_muts = which_muts
        self.which_libs = which_libs
        self.name = prefix

        self.N_BP = len(self.sequence)
        for i in xrange(len(self.primer_set)):
            self.primer_set[i] = RNA2DNA(self.primer_set[i])
        if not self.primer_set:
            assembly = Primer_Assembly(sequence)
            self.primer = assembly.primer_set
        if not self.which_muts:
            self.which_muts = range(1 - self.offset, self.N_BP + 1 - self.offset)

        self.is_error = False
        self.N_primers = len(self.primer_set)
        self.N_constructs = 1 + len(self.which_muts)
        self.N_plates = int(math.floor((self.N_constructs - 1) / 96.0) + 1)

        self.mutate_primers()


    def mutate_primers(self):
        (self.primers, self.is_error) = get_primer_index(self.primer_set, self.sequence)
        if self.is_error: return
        self.plates = [[Plate_96Well() for i in xrange(self.N_plates)] for i in xrange(self.N_primers)]
        print 'Filling out sequences ...\n'

        for p in xrange(self.N_primers):
            for l_pos in xrange(len(self.which_libs)):
                # lib should be a number: 1, 2, or 3 for the different possible mutations.
                lib = self.which_libs[l_pos]

                for m_pos in xrange(-1, len(self.which_muts)):
                    # which construct is this?
                    n = (1 + len(self.which_muts)) * (lib - 1) + m_pos + 1
                    plate_num = int(math.floor(n / 96.0))
                    plate_pos = n % 96 + 1
                    well_tag = num_to_coord(plate_pos)

                    # m is actual position along sequence
                    if m_pos == -1:
                        m = -1
                    else:
                        m = self.offset + self.which_muts[m_pos] - 1

                    if (m >= self.primers[0, p] and m <= self.primers[1, p]) or m == -1:
                        wt_primer = self.primer_set[p]
                        mut_primer = wt_primer
                        if m == -1:
                            well_name = 'Lib%d-WT' % lib
                        else:
                            if self.primers[2, p] == -1:
                                wt_primer = reverse_complement(wt_primer)
                                mut_primer = reverse_complement(mut_primer)

                            m_shift = int(m - self.primers[0, p])
                            mut_primer = list(mut_primer)
                            mut_primer[m_shift] = get_mutation(wt_primer[m_shift], lib)
                            mut_primer = ''.join(mut_primer)

                            # Name, e.g., "C75A".
                            well_name = 'Lib%d-%s%d%s' % (lib, wt_primer[m_shift], self.which_muts[m_pos], mut_primer[m_shift])

                            if self.primers[2, p] == -1:
                                wt_primer = reverse_complement(wt_primer)
                                mut_primer = reverse_complement(mut_primer)

                        self.plates[p][plate_num].set_well(well_tag, well_name, mut_primer)


    def print_constructs(self):
        for i in xrange(len(self.plates[0])):
            for j in xrange(len(self.plates)):
                print 'Plate \033[95m%d\033[0m; Primer \033[92m%d\033[0m' % (i + 1, j + 1)
                print self.plates[j][i].print_constructs(self.primer_set[j])


class Plate_96Well(object):
    def __init__(self):
        self.coords = set()
        self.data = {}


    def set_well(self, coord, tag, primer):
        if coord_to_num(coord) == -1:
            print 'Invalid 96 well coordinate: %s.' % coord
        else:
            self.coords.add(coord)
            self.data[coord_to_num(coord)] = (tag, primer)

    def get_well(self, coord):
        if coord_to_num(coord) == -1:
            print 'Invalid 96 well coordinate: %s.' % coord
            return
        else:
            if coord in self.coords:
                return self.data[coord_to_num(coord)]
            else:
                return

    def get_count(self):
        return len(self.coords)


    def print_constructs(self, ref_primer):
        string = ''
        for key in sorted(self.data):
            string += '\033[94m%s\033[0m' % num_to_coord(key).ljust(5)
            mut = self.data[key][0]
            if mut[-2:] == 'WT':
                string += ('%s\033[100m%s\033[0m' % (mut[:-2], mut[-2:])).ljust(28)
            else:
                string += ('%s\033[96m%s\033[0m\033[93m%s\033[0m\033[91m%s\033[0m' % (mut[:5], mut[5], mut[6:-1], mut[-1])).ljust(45)

            if ref_primer:
                for i in xrange(len(ref_primer)):
                    if ref_primer[i] != self.data[key][1][i]:
                        string += '\033[41m%s\033[0m' % self.data[key][1][i]
                    else:
                        string += self.data[key][1][i]

            else:
                string += self.data[key][1]
            string += '\n'

        if not string: string = '(empty)\n'
        return string


def design_primers_2D(sequence, primer_set=[], offset=0, which_muts=[], which_libs=[1], prefix='lib'):
    # plate = Mutate_Map(sequence, primer_set, offset, which_muts, which_libs, prefix)
    plate = Mutate_Map('TTCTAATACGACTCACTATAGGAACCGCGAGTAGCGGAAATCCAGTAGGAACACTATACTACTGGATAATCAAAGACAAATCTGCCCGAAGGGCTTGAGAACATCGAAACACGATGCAGAGGTGGCAGCCTCCGGTGGGTTAAAACCCAACGTTCTCAACAATAGTGAAAAGCGCGAGTAGCGCAACAAAGAAACAACAACAACAAC', ['TTCTAATACGACTCACTATAGGAACCG','CAGTAGTATAGTGTTCCTACTGGATTTCCGCTACTCGCGGTTCCTATAGTGAGTCGTA','TCCAGTAGGAACACTATACTACTGGATAATCAAAGACAAATCTGCCCGAAGGGCTTG','CCCACCGGAGGCTGCCACCTCTGCATCGTGTTTCGATGTTCTCAAGCCCTTCGGGCAGAT', 'AGCCTCCGGTGGGTTAAAACCCAACGTTCTCAACAATAGTGAAAAGCGCGAGTAGCGCAA', 'GTTGTTGTTGTTGTTTCTTTGTTGCGCTACTCGCGCTTTTCA'], 0, range(41, 168 + 1), [1], 'c1lig')
    plate.print_constructs()
    # plate.print_misprime()
    # if plate.is_solution:
    #     print plate.print_assembly()
    #     print plate.print_primers()
    #     print plate.print_warnings()
    # else:
    #     print '** No solution found!'


def main():
    if len(sys.argv) > 1:
        for i in xrange(1):
            t0 = time.time()
            design_primers_2D(sys.argv[1])
            print 'Time elapsed: %.1f s.' % (time.time() - t0)


if __name__ == "__main__":
    main()

