import math
import sys
import time

from util import *
from primerize_1d import *


class Mutate_Map(object):
    def __init__(self, sequence, primer_set=[], offset=0, which_muts=[], which_libs=[1], prefix='lib'):
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
            self.primer_set = assembly.primer_set
        if not self.which_muts:
            self.which_muts = range(1 - self.offset, self.N_BP + 1 - self.offset)
        self.construct_names = list(' ' * (len(self.which_muts) + 1))

        self.is_error = False
        self.N_primers = len(self.primer_set)
        self.N_constructs = 1 + len(self.which_muts)
        self.N_plates = int(math.floor((self.N_constructs - 1) / 96.0) + 1)

        self.mutate_primers()


    def mutate_primers(self):
        (self.primers, self.is_error) = get_primer_index(self.primer_set, self.sequence)
        if self.is_error: return
        self.plates = [[Plate_96Well() for i in xrange(self.N_plates)] for i in xrange(self.N_primers)]
        print 'Filling out sequences ...'

        for p in xrange(self.N_primers):
            for l_pos in xrange(len(self.which_libs)):
                # lib should be a number: 1, 2, or 3 for the different possible mutations.
                lib = self.which_libs[l_pos]

                for m_pos in xrange(-1, len(self.which_muts)):
                    # which construct is this?
                    n = m_pos + 1
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

                        self.construct_names[n] = well_name
                        self.plates[p][plate_num].set_well(well_tag, well_name, mut_primer)


    def print_constructs(self):
        output = ''
        for i in xrange(len(self.plates[0])):
            for j in xrange(len(self.plates)):
                output += 'Plate \033[95m%d\033[0m; Primer \033[92m%d\033[0m\n' % (i + 1, j + 1)
                output += self.plates[j][i].print_constructs(self.primer_set[j])
        return output

    def output_constructs(self, path='./'):
        save_construct_key(self.construct_names, self.name, path)

    def output_spreadsheet(self, path='./'):
        save_plates_excel(self.plates, self.N_plates, self.N_primers, self.name, path)


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

    def print_constructs(self, ref_primer=''):
        return print_primer_plate(self, ref_primer)


def design_primers_2D(sequence, primer_set=[], offset=0, which_muts=[], which_libs=[1], prefix='lib'):
    plate = Mutate_Map(sequence, primer_set, offset, which_muts, which_libs, prefix)
    if plate.is_error:
        print '** Invalid input primer_set!'
    else:
        print plate.print_constructs()
        plate.output_constructs()
        plate.output_spreadsheet()


def main():
    if len(sys.argv) > 1:
        for i in xrange(1):
            t0 = time.time()
            design_primers_2D(sys.argv[1])
            print 'Time elapsed: %.1f s.' % (time.time() - t0)


if __name__ == "__main__":
    main()

