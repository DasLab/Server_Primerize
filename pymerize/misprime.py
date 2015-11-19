import numpy

from util import *


def check_misprime(sequence):
    N = len(sequence)
    # length of string subsets
    m = 20
    subset_str = []

    # match to sequence
    for i in xrange(N):
        start_pos = max(i - m, 0) - 1
        if start_pos == -1:
            subset_str.append(sequence[i::-1])
        else:
            subset_str.append(sequence[i:start_pos:-1])

    # match to reverse complement of sequence
    sequence_rc = reverse_complement(sequence)
    for i in xrange(N):
        end_pos = N - i - 1
        start_pos = max(end_pos - m - 1, 0) - 1
        if start_pos == -1:
            subset_str.append(sequence_rc[end_pos::-1])
        else:
            subset_str.append(sequence_rc[end_pos:start_pos:-1])

    sort_idx = numpy.argsort(subset_str)
    subset_str.sort()

    # how close is match to neighbor?
    match_next = numpy.zeros((1, 2 * N - 1))
    misprime_score_next = numpy.zeros((1, 2 * N - 1))
    for i in xrange(2 * N - 1):
        count = -1
        misprime_score = 0
        str_1 = subset_str[i]
        str_2 = subset_str[i + 1]

        while (count < len(str_1) - 1 and count < len(str_2) - 1):
            if str_1[count + 1] != str_2[count + 1]:
                break
            count += 1

            if str_1[count] == 'G' or str_1[count] == 'C':
                misprime_score += 1.25
            else:
                misprime_score += 1.0

        match_next[0, i] = count
        misprime_score_next[0, i] = misprime_score

    match_max = numpy.zeros((1, 2 * N))
    best_match = numpy.zeros((1, 2 * N))
    misprime_score_max = numpy.zeros((1, 2 * N))

    # compare both neighbors
    match_max[0, 0] = match_next[0, 0]
    best_match[0, 0] = 1
    misprime_score_max[0, 0] = misprime_score_next[0, 0]

    match_max[0, 2 * N - 1] = match_next[0, 2 * N - 2]
    best_match[0, 2 * N - 1] = 2 * N - 2
    misprime_score_max[0, 2 * N - 1] = misprime_score_next[0, 2 * N - 2]

    for i in xrange(1, 2 * N - 1):
        if (match_next[0, i - 1] > match_next[0, i]):
            best_match[0, i] = i - 1
            match_max[0, i] = match_next[0, i - 1]
            misprime_score_max[0, i] = misprime_score_next[0, i - 1]
        else:
            best_match[0, i] = i + 1
            match_max[0, i] = match_next[0, i]
            misprime_score_max[0, i] = misprime_score_next[0, i]

    num_match_foward = numpy.zeros((1, N))
    misprime_score_forward = numpy.zeros((1, N))
    best_match_forward = numpy.zeros((1, N))
    num_match_reverse = numpy.zeros((1, N))
    misprime_score_reverse = numpy.zeros((1, N))
    best_match_reverse = numpy.zeros((1, N))

    for i in xrange(2 * N):
        if (sort_idx[i] <= N - 1):
            num_match_foward[0, sort_idx[i]] = match_max[0, i]
            misprime_score_forward[0, sort_idx[i]] = misprime_score_max[0, i]
            best_match_forward[0, sort_idx[i]] = (sort_idx[best_match[0, i]] - 1) % N + 1
        else:
            num_match_reverse[0, sort_idx[i] - N] = match_max[0, i]
            misprime_score_reverse[0, sort_idx[i] - N] = misprime_score_max[0, i]
            best_match_reverse[0, sort_idx[i] - N] = (sort_idx[best_match[0, i]] - 1) % N + 1

    return (num_match_foward, num_match_reverse, best_match_forward, best_match_reverse, misprime_score_forward, misprime_score_reverse)




