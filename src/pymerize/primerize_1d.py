import math
from numba import jit
import numpy
import sys
import time

from misprime import *
from thermo import *
from util import *


class Primer_Assembly(object):
    def __init__(self, sequence, min_Tm=60.0, NUM_PRIMERS=0, MIN_LENGTH=15, MAX_LENGTH=60, prefix='primer'):
        self.sequence = RNA2DNA(sequence)

        self.min_Tm = min_Tm
        self.NUM_PRIMERS = NUM_PRIMERS
        self.MIN_LENGTH = MIN_LENGTH
        self.MAX_LENGTH = MAX_LENGTH
        self.name = prefix

        self.N_BP = len(self.sequence)
        self.is_solution = True
        self.primers = []
        self.warnings = []
        self.Tm_overlaps = []

        self.COL_SIZE = 142
        self.WARN_CUTOFF = 3
        self.design_primers()


    def design_primers(self):
        print 'Precalculataing Tm matrix ...'
        self.Tm_precalculated = precalculate_Tm(self.sequence)
        print 'Precalculataing misprime score ...'
        (self.num_match_forward, self.num_match_reverse, self.best_match_forward, self.best_match_reverse, self.misprime_score_forward, self.misprime_score_reverse) = check_misprime(self.sequence)

        print 'Doing dynamics programming calculation ...'
        (self.scores_start, self.scores_stop, self.scores_final, self.choice_start_p, self.choice_start_q, self.choice_stop_i, self.choice_stop_j, self.MAX_SCORE, self.N_primers) = dynamic_programming(self.NUM_PRIMERS, self.MIN_LENGTH, self.MAX_LENGTH, self.min_Tm, self.N_BP, self.misprime_score_forward, self.misprime_score_reverse, self.Tm_precalculated)
        print 'Doing backtracking ...\n'
        (self.is_solution, self.primers, self.primer_set, self.warnings) = back_tracking(self.N_BP, self.sequence, self.scores_final, self.choice_start_p, self.choice_start_q, self.choice_stop_i, self.choice_stop_j, self.N_primers, self.MAX_SCORE, self.num_match_forward, self.num_match_reverse, self.best_match_forward, self.best_match_reverse, self.WARN_CUTOFF)
        if self.is_solution:
            (self.bp_lines, self.seq_lines, self.print_lines, self.Tm_overlaps) = draw_assembly(self.sequence, self.primers, self.name, self.COL_SIZE)
        else:
            (self.bp_lines, self.seq_lines, self.print_lines) = ([], [], [])


    def print_misprime(self):
        for i in xrange(int(math.floor(self.N_BP / self.COL_SIZE)) + 1):
            allow_forward_line = list(' ' * self.COL_SIZE)
            allow_reverse_line = list(' ' * self.COL_SIZE)
            sequence_line = list(' ' * self.COL_SIZE)

            for j in xrange(self.COL_SIZE):
                pos = i * self.COL_SIZE + j
                if (pos < self.N_BP - 1):
                    sequence_line[j] = self.sequence[pos]
                    allow_forward_line[j] = str(int(min(self.num_match_forward[0, pos] + 1, 9)))
                    allow_reverse_line[j] = str(int(min(self.num_match_reverse[0, pos] + 1, 9)))

            print '%s\n%s\n%s\n' % (''.join(allow_forward_line).strip(), ''.join(sequence_line).strip(), ''.join(allow_reverse_line).strip())


    def print_assembly(self):
        output = '\n'
        x = 0
        for i in xrange(len(self.print_lines)):
            (flag, string) = self.print_lines[i]
            if (flag == '$' and 'xx' in string):
                Tm = '%2.1f' % self.Tm_overlaps[x]
                output += string.replace('x' * len(Tm), '\033[41m%s\033[0m' % Tm) + '\n'
                x += 1
            elif (flag == '^' or flag == '!'):
                num = string.replace(' ', '').replace('A', '').replace('G', '').replace('C', '').replace('T', '').replace('-', '').replace('>', '').replace('<', '')
                output += string.replace(num, '\033[100m%s\033[0m' % num) + '\n'
            elif (flag == '~'):
                output += '\033[92m%s\033[0m' % string + '\n'
            elif (flag == '='):
                output += '\033[96m%s\033[0m' % string + '\n'
            else:
                output += string + '\n'
        return output


    def print_primers(self):
        output = '%s%s\tSEQUENCE\n' % ('PRIMERS'.ljust(20), 'LENGTH'.ljust(10))
        for i in xrange(len(self.primer_set)):
            name = '%s-\033[100m%s\033[0m%s' % (self.name, i + 1, primer_suffix(i))
            output += '%s%s\t%s\n' % (name.ljust(39), str(len(self.primer_set[i])).ljust(10), self.primer_set[i])
        return output + '\n'


    def print_warnings(self):
        output = ''
        for i in xrange(len(self.warnings)):
            warning = self.warnings[i]
            p_1 = '\033[100m%d\033[0m%s' % (warning[0], primer_suffix(warning[0] - 1))
            p_2 = ', '.join('\033[100m%d\033[0m%s' % (x, primer_suffix(x - 1)) for x in warning[3])
            output += '\033[93mWARNING\033[0m: Primer %s can misprime with %d-residue overlap to position %s, which is covered by primers: %s\n' % (p_1.rjust(4), warning[1], str(int(warning[2])).rjust(3), p_2)
        return output + '\n'


@jit(nopython=True, nogil=True, cache=True)
def dynamic_programming(NUM_PRIMERS, MIN_LENGTH, MAX_LENGTH, min_Tm, N_BP, misprime_score_forward, misprime_score_reverse, Tm_precalculated):
    # could be zero, meaning user does not know.
    num_primer_sets = int(NUM_PRIMERS / 2)
    num_primer_sets_max = int(math.ceil(N_BP / float(MIN_LENGTH)))

    misprime_score_weight = 10.0
    MAX_SCORE = N_BP * 2 + 1
    MAX_SCORE += misprime_score_weight * max(numpy.amax(misprime_score_forward), numpy.amax(misprime_score_reverse)) * 2 * num_primer_sets_max

    scores_start = MAX_SCORE * numpy.ones((N_BP, N_BP, num_primer_sets_max))
    scores_stop = MAX_SCORE * numpy.ones((N_BP, N_BP, num_primer_sets_max))
    scores_final = MAX_SCORE * numpy.ones((N_BP, N_BP, num_primer_sets_max))

    # used for backtracking:
    choice_start_p = numpy.zeros((N_BP, N_BP, num_primer_sets_max))
    choice_start_q = numpy.zeros((N_BP, N_BP, num_primer_sets_max))
    choice_stop_i = numpy.zeros((N_BP, N_BP, num_primer_sets_max))
    choice_stop_j = numpy.zeros((N_BP, N_BP, num_primer_sets_max))

    # basic setup -- first primer
    # First set is special.
    #  |                     p
    #  ---------------------->
    #                   ||||||
    #                   <-----...
    #                   q
    #
    for p in xrange(MIN_LENGTH, MAX_LENGTH + 1):
        # STOP[reverse](1)
        q_min = max(1, p - MAX_LENGTH + 1)
        q_max = p

        for q in xrange(q_min, q_max + 1):
            if (Tm_precalculated[q - 1, p - 1] > min_Tm):
                scores_stop[p - 1, q - 1, 0] = (q - 1) + 2 * (p - q + 1)
                scores_stop[p - 1, q - 1, 0] += misprime_score_weight * (misprime_score_forward[0, p - 1] + misprime_score_reverse[0, q - 1])

    best_min_score = MAX_SCORE
    n = 1
    while (n <= num_primer_sets_max):
        # final scoring -- let's see if we can 'close' at the end of the sequence.
        #
        #                 p
        #  --------------->
        #            ||||||
        #            <---------------------
        #            q                    N_BP
        #
        for p in xrange(1, N_BP + 1):
            q_min = max(1, p - MAX_LENGTH + 1)
            q_max = p

            # STOP[reverse]
            for q in xrange(q_min, q_max + 1):
                # previous primer ends had overlap with good Tm and were scored
                if (scores_stop[p - 1, q - 1, n - 1] < MAX_SCORE):
                    i = N_BP + 1
                    j = N_BP
                    last_primer_length = j - q + 1
                    if last_primer_length <= MAX_LENGTH and last_primer_length >= MIN_LENGTH:
                        scores_final[p - 1, q - 1, n - 1] = scores_stop[p - 1, q - 1, n - 1] + (i - p - 1)
                        scores_final[p - 1, q - 1, n - 1] += misprime_score_weight * (misprime_score_forward[0, p - 1] + misprime_score_reverse[0, q - 1])

        min_score = numpy.amin(scores_final[:, :, n - 1])
        if (min_score < best_min_score or n == 1):
            best_min_score = min_score
            best_n = n

        if (n >= num_primer_sets_max):
            break
        if (num_primer_sets > 0 and n == num_primer_sets):
            break

        # considering another primer set
        n += 1

        #
        #        p              i
        #  ------>              ------ ... ->
        #    |||||              ||||||
        #    <------------------------
        #    q                       j
        #
        for p in xrange(1, N_BP + 1):
            # STOP[forward](1)
            q_min = max(1, p - MAX_LENGTH + 1)
            q_max = p

            # STOP[reverse](1)
            for q in xrange(q_min, q_max + 1):
                # previous primer ends had overlap with good Tm and were scored
                if (scores_stop[p - 1, q - 1, n - 2] < MAX_SCORE):
                    # START[reverse](1)
                    min_j = max(p + 1, q + MIN_LENGTH - 1)
                    max_j = min(N_BP, q + MAX_LENGTH - 1)

                    for j in xrange(min_j, max_j + 1):
                        # start[reverse](2)
                        min_i = max(p + 1, j - MAX_LENGTH + 1)
                        max_i = j

                        for i in xrange(min_i, max_i + 1):
                            # at some PCR starge thiw will be an endpoint!
                            if (Tm_precalculated[i - 1, j - 1] > min_Tm):
                                potential_score = scores_stop[p - 1, q - 1, n - 2] + (i - p - 1) + 2 * (j - i + 1)
                                if (potential_score < scores_start[i - 1, j - 1, n - 2]):
                                    scores_start[i - 1, j - 1, n - 2] = potential_score
                                    choice_start_p[i - 1, j - 1, n - 2] = p - 1
                                    choice_start_q[i - 1, j - 1, n - 2] = q - 1

        #
        #             i                     p
        #             ---------------------->
        #             ||||||           ||||||
        #  <----------------           <----- ...
        #                  j           q
        #
    
        # START[reverse](1)
        for j in xrange(1, N_BP + 1):
            # START[reverse](2)
            min_i = max(1, j - MAX_LENGTH + 1)
            max_i = j

            for i in xrange(min_i, max_i + 1):
                # could also just make this 1:N_BP, but that would wast a little time.
                if (scores_start[i - 1, j - 1, n - 2] < MAX_SCORE):
                    # STOP[reverse](1)
                    min_p = max(j + 1, i + MIN_LENGTH - 1)
                    max_p = min(N_BP, i + MAX_LENGTH - 1)

                    for p in xrange(min_p, max_p + 1):
                        # STOP[reverse](2)
                        min_q = max(j + 1, p - MAX_LENGTH + 1)
                        max_q = p

                        for q in xrange(min_q, max_q + 1):
                            if (Tm_precalculated[q - 1, p - 1] > min_Tm):
                                potential_score = scores_start[i - 1, j - 1, n - 2] + (q - j - 1) + 2 * (p - q + 1)
                                potential_score += misprime_score_weight * (misprime_score_forward[0, p - 1] + misprime_score_reverse[0, q - 1])
                                if (potential_score < scores_stop[p - 1, q - 1, n - 1]):
                                    scores_stop[p - 1, q - 1, n - 1] = potential_score
                                    choice_stop_i[p - 1, q - 1, n - 1] = i - 1
                                    choice_stop_j[p - 1, q - 1, n - 1] = j - 1

    if (num_primer_sets > 0):
        N_primers = num_primer_sets
    else:
        N_primers = best_n
    return (scores_start, scores_stop, scores_final, choice_start_p, choice_start_q, choice_stop_i, choice_stop_j, MAX_SCORE, N_primers)


def back_tracking(N_BP, sequence, scores_final, choice_start_p, choice_start_q, choice_stop_i, choice_stop_j, N_primers, MAX_SCORE, num_match_forward, num_match_reverse, best_match_forward, best_match_reverse, WARN_CUTOFF):
    y = numpy.amin(scores_final[:, :, N_primers - 1], axis=0)
    idx = numpy.argmin(scores_final[:, :, N_primers - 1], axis=0)
    min_scroe = numpy.amin(y)
    q = numpy.argmin(y)
    p = idx[q]

    is_solution = True
    primer_set = []
    misprime_warn = []
    primers = numpy.zeros((3, 2 * N_primers))
    if (min_scroe == MAX_SCORE):
        is_solution = False
    else:
        primers[:, 2 * N_primers - 1] = [q, N_BP - 1, -1]
        for m in xrange(N_primers - 1, 0, -1):
            i = choice_stop_i[p, q, m]
            j = choice_stop_j[p, q, m]
            primers[:, 2 * m] = [i, p, 1]
            p = choice_start_p[i, j, m - 1]
            q = choice_start_q[i, j, m - 1]
            primers[:, 2 * m - 1] = [q, j, -1]
        primers[:, 0] = [0, p, 1]
        primers = primers.astype(int)

        for i in xrange(2 * N_primers):
            primer_seq = sequence[primers[0, i]:primers[1, i] + 1]
            if primers[2, i] == -1:
                primer_set.append(reverse_complement(primer_seq))

                # mispriming "report"
                end_pos = primers[0, i]
                if (num_match_reverse[0, end_pos] >= WARN_CUTOFF):
                    problem_primer = find_primers_affected(primers, best_match_reverse[0, end_pos])
                    misprime_warn.append((i + 1, num_match_reverse[0, end_pos] + 1, best_match_reverse[0, end_pos] + 1, problem_primer))
            else:
                primer_set.append(str(primer_seq))

                # mispriming "report"
                end_pos = primers[1, i]
                if (num_match_forward[0, end_pos] >= WARN_CUTOFF):
                    problem_primer = find_primers_affected(primers, best_match_forward[0, end_pos])
                    misprime_warn.append((i + 1, num_match_forward[0, end_pos] + 1, best_match_forward[0, end_pos] + 1, problem_primer))

    return (is_solution, primers, primer_set, misprime_warn)


def find_primers_affected(primers, pos):
    primer_list = []
    for i in xrange(primers.shape[1]):
        if (pos >= primers[0, i] and pos <= primers[1, i]):
            primer_list.append(i + 1)
    return primer_list


def design_primers_1D(sequence, min_Tm=60, NUM_PRIMERS=0, MIN_LENGTH=15, MAX_LENGTH=60, prefix='primer'):
    assembly = Primer_Assembly(sequence, min_Tm, NUM_PRIMERS, MIN_LENGTH, MAX_LENGTH, prefix)
    assembly.print_misprime()
    if assembly.is_solution:
        print assembly.print_assembly()
        print assembly.print_primers()
        print assembly.print_warnings()
    else:
        print '** No solution found!'


def main():
    if len(sys.argv) > 1:
        for i in xrange(1):
            t0 = time.time()
            design_primers_1D(sys.argv[1])
            print 'Time elapsed: %.1f s.' % (time.time() - t0)


if __name__ == "__main__":
    main()

