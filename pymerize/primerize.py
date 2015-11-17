import math
import numpy
import sys

from misprime import *
from thermo import *
from util import *


class Primer_Assembly:
    def __init__(self, sequence, min_Tm, NUM_PRIMERS, MIN_LENGTH,MAX_LENGTH, prefix):
        self.sequence = RNA2DNA(sequence)

        self.N_BP = len(self.sequence)
        self.min_Tm = min_Tm
        self.NUM_PRIMERS = NUM_PRIMERS
        self.MIN_LENGTH = MIN_LENGTH
        self.MAX_LENGTH = MAX_LENGTH
        self.name = prefix
        self.design_primers()


    def design_primers(self):
        print 'Precalculataing Tm matrix... ',
        self.Tm_precalculated = precalculate_Tm(self.sequence)
        print 'Done!'

        print 'Precalculataing misprime score... ',
        (self.num_match_foward, self.num_match_reverse, self.best_match_forward, self.best_match_reverse, self.misprime_score_forward, self.misprime_score_reverse) = check_misprime(self.sequence)
        print 'Done!'

        print 'Doing dynamics programming calculation... ',
        self.dynamic_programming()
        print 'Done!'


    def dynamic_programming(self):
        # could be zero, meaning user does not know.
        num_primer_sets = self.NUM_PRIMERS / 2
        num_primer_sets_max = math.ceil(self.N_BP / self.MIN_LENGTH)

        MAX_SCORE = self.N_BP * 2 + 1
        misprime_score_weight = 10.0
        MAX_SCORE += misprime_score_weight * max(numpy.amax(self.misprime_score_forward), numpy.amax(self.misprime_score_reverse)) * 2 * num_primer_sets_max

        scores_start = MAX_SCORE * numpy.ones((self.N_BP, self.N_BP, num_primer_sets_max))




    def print_misprime(self):
        COL_SIZE = 150

        for i in range(int(math.floor(self.N_BP / COL_SIZE)) + 1):
            allow_forward_line = list(' ' * COL_SIZE)
            allow_reverse_line = list(' ' * COL_SIZE)
            sequence_line = list(' ' * COL_SIZE)

            for j in range(COL_SIZE):
                pos = i * COL_SIZE + j
                if (pos < self.N_BP - 1):
                    sequence_line[j] = self.sequence[pos]
                    allow_forward_line[j] = str(int(min(self.num_match_foward[0, pos] + 1, 9)))
                    allow_reverse_line[j] = str(int(min(self.num_match_reverse[0, pos] + 1, 9)))

            print '%s\n%s\n%s\n\n' % (''.join(allow_forward_line).strip(), ''.join(sequence_line).strip(), ''.join(allow_reverse_line).strip())


def design_primers_1D(sequence, min_Tm=60, NUM_PRIMERS=0, MIN_LENGTH=15,MAX_LENGTH=60, prefix='primer'):
    assembly = Primer_Assembly(sequence, min_Tm, NUM_PRIMERS, MIN_LENGTH, MAX_LENGTH, prefix)
    assembly.print_misprime()



def main():
    if len(sys.argv) > 1:
        design_primers_1D(sys.argv[1])


if __name__ == "__main__":
    main()