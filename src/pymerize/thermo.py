import math
import numpy

numpy.seterr('ignore')


class Nearest_Neighbor(object):
    def __init__(self):
        self.T = 273.15 + 37

        # From SantaLucia, Jr, Ann Rev 2004
        # A C G T
        self.delH_NN = numpy.array([
            [-7.6, -8.4, -7.8, -7.2],
            [-8.5, -8.0, -9.8, -7.8],
            [-8.2, -9.8, -8.0, -8.4],
            [-7.2, -8.2, -8.5, -7.6]
            ])
        self.delS_NN = numpy.array([
            [-21.3, -22.4, -21.0, -20.4],
            [-22.7, -19.9, -24.4, -21.0],
            [-22.2, -24.4, -19.9, -22.4],
            [-21.3, -22.2, -22.7, -21.3]
            ])
        self.delG_NN = self.delH_NN - (self.T * self.delS_NN) / 1000

        # From SantaLucia, Jr, Ann Rev 2004
        self.delH_AT_closing_penalty = numpy.array([2.2, 0.0, 0.0, 2.2])
        self.delS_AT_closing_penalty = numpy.array([6.9, 0.0, 0.0, 6.9])
        self.delG_AT_closing_penalty = self.delH_AT_closing_penalty - (self.T * self.delS_AT_closing_penalty) / 1000

        # Following also from Santaucia/Hicks.
        # They didn't compile delH and delS, so I should probably go
        # back to the original references. Pain in the ass!
        self.delH_mismatch = numpy.zeros((4, 4, 4))
        # AX/TY
        self.delH_mismatch[:, :, 0] = [
            [ 1.2,  2.3, -0.6, -7.6],
            [ 5.3,  0.0, -8.4,  0.7],
            [-0.7, -7.8, -3.1,  1.0],
            [-7.2, -1.2, -2.5, -2.7]
            ]
        # CX/GY
        self.delH_mismatch[:, :, 1] = [
            [-0.9,   1.9, -0.7, -8.5],
            [ 0.6,  -1.5, -8.0, -0.8],
            [-4.0, -10.6, -4.9, -4.1],
            [-7.8,  -1.5, -2.8, -5.0]
            ]
        # GX/CY
        self.delH_mismatch[:, :, 2] = [
            [-2.9,  5.2, -0.6, -8.2],
            [-0.7,  3.6, -9.8,  2.3],
            [ 0.5, -8.0, -6.0,  3.3],
            [-8.4,  5.2, -4.4, -2.2]
            ]
        # TX/AY
        self.delH_mismatch[:, :, 3] = [
            [ 4.7,  3.4,  0.7, -7.2],
            [ 7.6,  6.1, -8.2,  1.2],
            [ 3.0, -8.5,  1.6, -0.1],
            [-7.6,  1.0, -1.3,  0.2]
            ]

        self.delS_mismatch = numpy.zeros((4, 4, 4))
        # AX/TY
        self.delS_mismatch[:, :, 0] = [
            [  1.7,   4.6,  -2.3, -21.3],
            [ 14.6,  -4.4, -22.4,   0.2],
            [ -2.3, -21.0,  -9.5,   0.9],
            [-20.4,  -6.2,  -8.3, -10.8]
            ]
        # CX/GY
        self.delS_mismatch[:, :, 1] = [
            [ -4.2,   3.7,  -2.3, -22.7],
            [ -0.6,  -7.2, -19.9,  -4.5],
            [-13.2, -27.2, -15.3, -11.7],
            [-21.0,  -6.1,  -8.0, -15.8]
            ]
        # GX/CY
        self.delS_mismatch[:, :, 2] = [
            [ -9.8,  14.2,  -1.0, -22.2],
            [ -3.8,   8.9, -24.4,   5.4],
            [  3.2, -19.9, -15.8,  10.4],
            [-22.4,  13.5, -12.3,  -8.4]
            ]
        # TX/AY
        self.delS_mismatch[:, :, 3] = [
            [ 12.9,   8.0,   0.7, -21.3],
            [ 20.2,  16.4, -22.2,   0.7],
            [  7.4, -22.7,   3.6,  -1.7],
            [-21.3,   0.7,  -5.3,  -1.5]
            ]

        self.delG_mismatch = numpy.zeros((4, 4, 4))
        # AX/TY
        self.delG_mismatch[:, : ,0] = [
            [ 0.61,  0.88,  0.14, -1.00],
            [ 0.77,  1.33, -1.44,  0.64],
            [ 0.02, -1.28, -0.13,  0.71],
            [-0.88,  0.73,  0.07,  0.69]
            ]
        # CX/GY
        self.delG_mismatch[:, :, 1] = [
            [ 0.43,  0.75,  0.03, -1.45],
            [ 0.79,  0.70, -1.84,  0.62],
            [ 0.11, -2.17, -0.11, -0.47],
            [-1.28,  0.40, -0.32, -0.13]
            ]
        # GX/CY
        self.delG_mismatch[:, :, 2] = [
            [ 0.17,  0.81, -0.25, -1.30],
            [ 0.47,  0.79, -2.24,  0.62],
            [-0.52, -1.84, -1.11,  0.08],
            [-1.44,  0.98, -0.59,  0.45]
            ]
        # TX/AY
        self.delG_mismatch[:, :, 3] = [
            [ 0.69,  0.92,  0.42, -0.58],
            [ 1.33,  1.05, -1.30,  0.97],
            [ 0.74, -1.45,  0.44,  0.43],
            [-1.00,  0.75,  0.34,  0.68]
            ]

        self.delH_init = 0.2
        self.delS_init = -5.7


def convert_sequence(sequence):
    # Easier to keep track of integers in Matlab
    # A,C,G,T --> 1,2,3,4.
    sequence = sequence.upper()
    numerical_sequence = numpy.zeros((1, len(sequence)), dtype=numpy.int_)
    seq2num_dict = {'A': 0, 'C': 1, 'G': 2, 'U': 3, 'T': 3}

    for i in xrange(len(sequence)):
        numerical_sequence[0, i] = seq2num_dict[sequence[i]]
    return numerical_sequence


def ionic_strength_correction(Tm, monovalent_conc, divalent_conc, f_GC, N_BP):
    # From Owczarzy et al., Biochemistry, 2008.
    R = math.sqrt(divalent_conc) / monovalent_conc
    Tm_corrected = Tm
    if (R < 0.22):
        # Monovalent dominated
        x = math.log(monovalent_conc)
        Tm_corrected = 1.0 / ((1.0 / Tm) + (4.29 * f_GC - 3.95) * 1e-5 * x + 9.40e-6 * math.pow(x, 2))
    else:
        # Divalent dominated
        (a, b, c, d, e, f, g) = (3.92e-5, -9.11e-6, 6.26e-5, 1.42e-5, -4.82e-4, 5.25e-4, 8.31e-5)

        if (R < 6.0):
            # Some competition from monovalent
            y = monovalent_conc
            a *= (0.843 - 0.352 * math.sqrt(y) * math.log(y))
            d *= (1.279 - 4.03e-3 * math.log(y) - 8.03e-3 * math.pow(math.log(y), 2))
            g *= (0.486 - 0.258 * math.log(y) + f * 10 * math.pow(math.log(y), 3))

        x = math.log(divalent_conc)
        Tm_corrected = 1.0 / ((1.0 / Tm) + a + b * x + f_GC * (c + d * x) + (1.0 / (2 * (N_BP - 1))) * (e + f * x + g * math.pow(x, 2)))
    return Tm_corrected


def precalculate_Tm(sequence, DNA_conc=0.2e-6, monovalent_conc=0.1, divalent_conc=0.0015):
    # This could be sped up significantly, since many of the sums of
    # delH, delG are shared between calculations.
    numerical_sequence = convert_sequence(sequence)
    NN_parameters = Nearest_Neighbor()
    delS_DNA_conc = 1.987 * math.log(DNA_conc / 2)
    delS_init = NN_parameters.delS_init + delS_DNA_conc
    N_BP = len(sequence)

    delH_matrix = NN_parameters.delH_init * numpy.ones((N_BP, N_BP))
    delS_matrix = delS_init * numpy.ones((N_BP, N_BP))
    f_GC = numpy.zeros((N_BP, N_BP))
    len_BP = numpy.ones((N_BP, N_BP))

    for i in xrange(N_BP):
        if (numerical_sequence[0, i] in (1, 2)):
            f_GC[i, i] = 1

    print 'Filling delH, delS matrix ...'
    for i in xrange(N_BP):
        for j in xrange(i + 1, N_BP):
            delH_matrix[i, j] = delH_matrix[i, j - 1] + NN_parameters.delH_NN[numerical_sequence[0, j - 1], numerical_sequence[0, j]]
            delS_matrix[i, j] = delS_matrix[i, j - 1] + NN_parameters.delS_NN[numerical_sequence[0, j - 1], numerical_sequence[0, j]]
            len_BP[i, j] = len_BP[i, j - 1] + 1

            f_GC[i, j] = f_GC[i, j - 1]
            if (numerical_sequence[0, j] in (1, 2)):
                f_GC[i, j] += 1

    print 'Terminal penalties ...'
    for i in xrange(N_BP):
        for j in xrange(i + 1, N_BP):
            delH_matrix[i, j] += NN_parameters.delH_AT_closing_penalty[numerical_sequence[0, i]]
            delH_matrix[i, j] += NN_parameters.delH_AT_closing_penalty[numerical_sequence[0, j]]

            delS_matrix[i, j] += NN_parameters.delS_AT_closing_penalty[numerical_sequence[0, i]]
            delS_matrix[i, j] += NN_parameters.delS_AT_closing_penalty[numerical_sequence[0, j]]

    Tm = 1000 * numpy.divide(delH_matrix, delS_matrix)
    f_GC = numpy.divide(f_GC, len_BP)

    print 'Ionic strength corrections ...'
    for i in xrange(N_BP):
        for j in xrange(i, N_BP):
            Tm[i, j] = ionic_strength_correction(Tm[i, j], monovalent_conc, divalent_conc, f_GC[i, j], len_BP[i, j])

    return Tm - 273.15


def calc_Tm(sequence, DNA_conc=1e-5, monovalent_conc=1.0, divalent_conc=0.0):
    numerical_sequence = convert_sequence(sequence)
    NN_parameters = Nearest_Neighbor()
    delS_DNA_conc = 1.987 * math.log(DNA_conc / 2)
    delS_sum = NN_parameters.delS_init + delS_DNA_conc
    delH_sum = NN_parameters.delH_init
    N_BP = len(sequence)

    for i in xrange(N_BP - 1):
        delH_sum += NN_parameters.delH_NN[numerical_sequence[0, i], numerical_sequence[0, i + 1]]
        delS_sum += NN_parameters.delS_NN[numerical_sequence[0, i], numerical_sequence[0, i + 1]]

    delH_sum += NN_parameters.delH_AT_closing_penalty[numerical_sequence[0, 0]]
    delH_sum += NN_parameters.delH_AT_closing_penalty[numerical_sequence[0, -1]]
    delS_sum += NN_parameters.delS_AT_closing_penalty[numerical_sequence[0, 0]]
    delS_sum += NN_parameters.delS_AT_closing_penalty[numerical_sequence[0, -1]]

    Tm = 1000 * delH_sum / delS_sum
    f_GC = (numpy.sum(numerical_sequence == 1) + numpy.sum(numerical_sequence == 2)) / float(N_BP)
    Tm = ionic_strength_correction(Tm, monovalent_conc, divalent_conc, f_GC, N_BP)
    return Tm - 273.15



