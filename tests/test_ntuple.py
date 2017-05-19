#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_ntuple
----------------------------------

Tests for TOPAS ntuple reading.
"""

# system imports
import unittest
import os.path

# third-party imports
import numpy as np
from numpy.testing import assert_array_almost_equal
from numpy.lib.recfunctions import append_fields

# project imports
from topas2numpy import read_ntuple


data_dir = 'tests/data'
ascii_path = os.path.join(data_dir, 'ascii-phasespace.phsp')
binary_path = os.path.join(data_dir, 'binary-phasespace.phsp')
limited_path = os.path.join(data_dir, 'limited-phasespace.phsp')
ascii_other_path = os.path.join(data_dir, 'ascii-other-ntuple.phsp')
binary_other_path = os.path.join(data_dir, 'binary-other-ntuple.phsp')

column_names = (
    'Position X (cm)',
    'Position Y (cm)',
    'Position Z (cm)',
    'Direction Cosine X',
    'Direction Cosine Y',
    'Energy (MeV)',
    'Weight',
    'Particle Type (in PDG Format)',
    'Flag to tell if Third Direction Cosine is Negative (1 means true)',
    'Flag to tell if this is the First Scored Particle from this History (1 means true)',
)

column_names_limited = (
    'Particle Type (sign from z direction)',
    'Energy (MeV) (-ve if new history)',
    'Position X (cm)',
    'Position Y (cm)',
    'Position Z (cm)',
    'Direction Cosine X',
    'Direction Cosine Y',
    'Weight',
)

other_column_names = (
    'Local position X [cm]',
    'Local position Y [cm]',
    'Local position Z [cm]',
    'Wavelength [nm]',
    'Arrival time [ns]',
    'ProcessID: 1 Scintillation, 2 Cerenkov, 3 Absorption',
)


class CommonTests(object):
    def test_column_names(self):
        self.assertEqual(self.result.dtype.names, self.column_names)

    def test_size(self):
        self.assertEqual(self.result.size, 104)


class TestAsciiNtuple(unittest.TestCase, CommonTests):
    def setUp(self):
        self.result = read_ntuple(ascii_path)
        self.column_names = column_names


class TestBinaryNtuple(unittest.TestCase, CommonTests):
    def setUp(self):
        self.result = read_ntuple(binary_path)
        self.column_names = column_names


class TestLimitedNtuple(unittest.TestCase, CommonTests):
    def setUp(self):
        self.result = read_ntuple(limited_path)
        self.column_names = column_names_limited


class TestCompare(unittest.TestCase):
    def setUp(self):
        self.ascii = read_ntuple(ascii_path)
        self.binary = read_ntuple(binary_path)
        self.limited = read_ntuple(limited_path)

    def test_compare_ascii_to_binary(self):
        for col in self.ascii.dtype.names:
            assert_array_almost_equal(self.ascii[col], self.binary[col],
                                      decimal=3)

    def test_compare_ascii_to_limited(self):

        # c = a * (b ? -1 : +1)
        a_name = 'Energy (MeV)'
        b_name = 'Flag to tell if this is the First Scored Particle from this History (1 means true)'
        c_name = 'Energy (MeV) (-ve if new history)'
        c = np.copy(self.ascii[a_name])
        c[self.ascii[b_name].astype('bool')] *= -1
        self.ascii = append_fields(self.ascii, c_name, c)

        # too much hassle to convert particle types to IAEA format
        excluded = ['Particle Type (sign from z direction)']
        checked = [s for s in self.limited.dtype.names if s not in excluded]

        for col in checked:
            assert_array_almost_equal(self.ascii[col], self.limited[col],
                                      decimal=3)


class CommonOtherTests(object):
    def test_column_names(self):
        self.assertEqual(self.result.dtype.names, other_column_names)

    def test_size(self):
        self.assertEqual(self.result.size, 1587)


class TestAsciiOtherNtuple(unittest.TestCase, CommonOtherTests):
    def setUp(self):
        self.result = read_ntuple(ascii_other_path)


class TestBinaryOtherNtuple(unittest.TestCase, CommonOtherTests):
    def setUp(self):
        self.result = read_ntuple(binary_other_path)


if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())
