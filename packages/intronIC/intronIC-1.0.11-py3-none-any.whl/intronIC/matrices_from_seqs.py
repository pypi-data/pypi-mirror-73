from collections import defaultdict
import re

def format_matrix(matrix, label="frequencies", precision=None):
    """
    Formats the contents of a matrix in FASTA
    format, with the first line being the
    order of characters, {index_order}, and the
    following lines containing the frequency of
    each character; each position in the sequence
    has its own line in the matrix.

    {label} is used as the header for the frequencies
    entry.

    example output:

    >{index_order}
    A C G T
    >{label}
    0.25 0.5 0.25 0.0
    0.0 0.75 0.25 0.0
    ...

    """
    string_list = []
    characters = sorted(matrix.keys())
    freq_index = defaultdict(list)
    for character, frequencies in sorted(matrix.items()):
        for i, e in sorted(frequencies.items()):
            if precision:
                e = round(e, precision)
            freq_index[i].append(str(e))
    start_index = min(freq_index.keys())
    char_order = '\t'.join(characters)
    # string_list.append(">index_order\n{}".format(character_order))
    string_list.append(">{}\tstart={}\n{}".format(label, start_index, char_order))
    for i, freqs in sorted(freq_index.items()):
        string_list.append('\t'.join(freqs))
        
    return '\n'.join(string_list)


def write_matrix_file(matrices, fn, precision=None):
    """
    Writes one or more matrices to a file, using
    keys as headers.

    """
    with open(fn, 'w') as outfile:
        for name, matrix in sorted(matrices.items()):
            label = '-'.join(name)
            # outfile.write('[#] {}\n'.format('-'.join(name)))
            outfile.write(format_matrix(matrix, label, precision) + '\n')


def matrix_from_seqs(seqs, start_index=0):
    """
    Constructs a position-weight matrix from one or
    more sequences.

    Returns a dictionary of {character: [f1, f2...fn]},
    where fn is the character frequency at the nth
    position in the sequence.

    """
    matrix = defaultdict(list)
    characters = set(['G', 'T', 'A', 'C'])
    lengths = set()
    n_seqs = 0

    for s in seqs:
        lengths.add(len(s))
        n_seqs += 1
        for i, e in enumerate(s, start=start_index):
            matrix[i].append(e)
            characters.add(e)
    
    if n_seqs == 0:
        return {}, 0

    character_order = sorted(characters)
    seq_length = min(lengths)

    frequencies = defaultdict(dict)

    for i in range(start_index, seq_length - abs(start_index)):
        chars = matrix[i]
        freqs = []
        for c in character_order:
            n = chars.count(c)
            f = n / n_seqs
            freqs.append(f)
            frequencies[c][i] = f

    return frequencies, n_seqs


def aggregate_seqs(
    seqfile, 
    five_bounds=(-20, 20), 
    three_bounds=(-20, 20), 
    blank=re.compile(r'[.\-*\s]')
):
    five_start, five_stop = five_bounds
    three_start, three_stop = three_bounds
    with open(seqfile) as f:
        for i, l in enumerate(f):
            bits = l.strip().split('\t')
            uid, score, five, seq, three = bits[:5]
            if blank.match(uid):
                uid = 'training_intron_{}'.format(i)
            five_seq = five[-five_flank:]
            three_seq = three[:three_flank]
