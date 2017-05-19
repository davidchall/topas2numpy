# -*- coding: utf-8 -*-

# system imports
import re
import os.path

# third-party imports
import numpy as np

re_uint = '\d+'
re_str = '[\S+ \t]+'

binary_old_int_columns = [
    'Particle Type (in PDG Format)',
    'Run ID',
    'Event ID',
    'Track ID',
    'Parent ID',
    'Seed Part 1',
    'Seed Part 2',
    'Seed Part 3',
    'Seed Part 4',
]

limited_col_names = [
    ('Particle Type (sign from z direction)', np.int8),
    ('Energy (MeV) (-ve if new history)', 'f'),
    ('Position X (cm)', 'f'),
    ('Position Y (cm)', 'f'),
    ('Position Z (cm)', 'f'),
    ('Direction Cosine X', 'f'),
    ('Direction Cosine Y', 'f'),
    ('Weight', 'f'),
]


def read_ntuple(filepath):
    root, ext = os.path.splitext(filepath)
    ntuple_path = root + '.phsp'
    header_path = root + '.header'

    file_format, col_names = _sniff_format(header_path)

    if file_format == 'ascii':
        # preserve column names => cannot be viewed as a np.recarray
        # http://docs.scipy.org/doc/numpy-1.10.1/user/basics.io.genfromtxt.html#validating-names
        return np.genfromtxt(ntuple_path, names=col_names, deletechars=set(), replace_space='')

    elif file_format == 'binary':
        return np.fromfile(ntuple_path, dtype=np.dtype(col_names))

    else:
        raise IOError('Unrecognized file format: "%s"' % filepath)


def _sniff_format(header_path):
    with open(header_path) as f:
        first_line = f.readline()

    # recognize limited phasespace
    if '$TITLE:' in first_line:
        return 'binary', limited_col_names

    read_ascii = 'Columns of data are as follows:'
    re_ascii = '^\s?{u}\s?: (?P<name>{s})'
    re_ascii = re.compile(re_ascii.format(u=re_uint, s=re_str))

    read_binary = 'Byte order of each record is as follows:'
    re_binary_old = '^\s?(?P<startbyte>{u})\s?-\s?(?P<endbyte>{u})\s?: (?P<name>{s})'
    re_binary_old = re.compile(re_binary_old.format(u=re_uint, s=re_str))
    re_binary_new = '^(?P<dtype>[bfi]{u}): (?P<name>{s})'
    re_binary_new = re.compile(re_binary_new.format(u=re_uint, s=re_str))

    col_names = []
    with open(header_path) as f:
        read_activated = False
        for line in f:
            if line.strip() in (read_ascii, read_binary):
                read_activated = True
                file_format = 'ascii' if read_ascii in line else 'binary'
                continue

            if read_activated:
                match_ascii = re_ascii.search(line)
                match_binary_new = re_binary_new.search(line)
                match_binary_old = re_binary_old.search(line)

                if match_ascii:
                    col_names.append(match_ascii.group('name').strip())

                # new-style headers use "f4: Name" format
                elif match_binary_new:
                    name = match_binary_new.group('name').strip()
                    dtype = match_binary_new.group('dtype').strip()
                    col_names.append((name, dtype))

                # old-style headers use " 0- 3: Name" format
                elif match_binary_old:
                    name = match_binary_old.group('name').strip()
                    b1 = int(match_binary_old.group('startbyte'))
                    b2 = int(match_binary_old.group('endbyte'))
                    n_bytes = b2-b1+1

                    dtype = 'f'
                    if n_bytes == 1:
                        dtype = 'b'
                    elif name in binary_old_int_columns:
                        dtype = 'i'
                    dtype = dtype + str(n_bytes)

                    col_names.append((name, dtype))

                else:
                    read_activated = False

    return file_format, col_names
