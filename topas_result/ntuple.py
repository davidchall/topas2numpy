# -*- coding: utf-8 -*-

# system imports
import re
import os.path

# third party imports
import numpy as np

re_uint = '\d+'
re_str = '[\S+ \t]+'


def read_ntuple(filepath):
    root, ext = os.path.splitext(filepath)
    ntuple_path = root + '.phsp'
    header_path = root + '.header'

    file_format = _read_format(header_path)
    if file_format == 'ascii':
        return _read_ascii(ntuple_path, header_path)
    elif file_format == 'binary':
        return _read_binary(ntuple_path, header_path)
    elif file_format == 'limited':
        return _read_limited(ntuple_path)
    else:
        message = 'Unrecognized file format: "%s"' % filepath
        raise IOError(message)


def _read_format(header_path):
    with open(header_path) as f:
        first_line = f.readline()

    if 'TOPAS ASCII Phase Space' in first_line:
        return 'ascii'
    elif 'TOPAS Binary Phase Space' in first_line:
        return 'binary'
    elif '$TITLE:' in first_line:
        return 'limited'


def _read_ascii(ntuple_path, header_path):
    col_names = []
    col_desc_marker = 'Columns of data are as follows:'
    re_tot = '\s?(?P<column>{u})\s?: (?P<name>{s})'
    regex = re.compile(re_tot.format(u=re_uint, s=re_str))

    with open(header_path) as f:
        read_col_names = False
        for line in f:
            if col_desc_marker in line:
                read_col_names = True
                continue

            if read_col_names:
                match = regex.search(line)
                if match:
                    col_names.append(match.group('name').strip())
                else:
                    read_col_names = False

    # preserve column names => cannot be viewed as a np.recarray
    # http://docs.scipy.org/doc/numpy-1.10.1/user/basics.io.genfromtxt.html#validating-names
    return np.genfromtxt(ntuple_path, names=col_names,
                         deletechars='', replace_space='')


def _read_binary(ntuple_path, header_path):
    col_types = []
    col_desc_marker = 'Byte order of each record is as follows:'
    re_tot = '\s?(?P<startbyte>{u})\s?-\s?(?P<endbyte>{u})\s?: (?P<name>{s})'
    regex = re.compile(re_tot.format(u=re_uint, s=re_str))

    with open(header_path) as f:
        read_col_names = False
        for line in f:
            if col_desc_marker in line:
                read_col_names = True
                continue

            if read_col_names:
                match = regex.search(line)
                if match:
                    name = match.group('name').strip()
                    b1 = int(match.group('startbyte'))
                    b2 = int(match.group('endbyte'))
                    n_bytes = b2-b1+1

                    dtype = 'f'
                    if n_bytes == 1:
                        dtype = 'b'
                    elif 'Particle Type' in name:
                        dtype = 'i'
                    dtype = dtype + str(n_bytes)

                    col_types.append((name, dtype))

                else:
                    read_col_names = False

    return np.fromfile(ntuple_path, dtype=np.dtype(col_types))


def _read_limited(ntuple_path):
    col_types = [
        ('Particle Type (sign from z direction)', np.int8),
        ('Energy (MeV) (-ve if new history)', 'f'),
        ('Position X (cm)', 'f'),
        ('Position Y (cm)', 'f'),
        ('Position Z (cm)', 'f'),
        ('Direction Cosine X', 'f'),
        ('Direction Cosine Y', 'f'),
        ('Weight', 'f'),
    ]

    return np.fromfile(ntuple_path, dtype=np.dtype(col_types))
