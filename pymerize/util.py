
def DNA2RNA(sequence):
    return sequence.upper().replace('T', 'U')


def RNA2DNA(sequence):
    return sequence.upper().replace('U', 'T')


def reverse_complement(sequence):
    sequence = list(sequence)
    sequence.reverse()

    rc_dict = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
    for i in range(len(sequence)):
        sequence[i] = rc_dict[sequence[i]]
    return ''.join(sequence)


