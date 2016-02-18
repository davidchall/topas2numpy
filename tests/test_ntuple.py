#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_ntuple
----------------------------------

Tests for TOPAS ntuple reading.
"""

import unittest
import os.path

from topas_result import read_ntuple

data_dir = 'tests/data'

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


class TestAscii(unittest.TestCase):

    def setUp(self):
        filepath = os.path.join(data_dir, 'ascii-phasespace.phsp')
        self.result = read_ntuple(filepath)

    def test_column_names(self):
        self.assertEqual(self.result.dtype.names, column_names)


class TestBinary(unittest.TestCase):

    def setUp(self):
        filepath = os.path.join(data_dir, 'binary-phasespace.phsp')
        self.result = read_ntuple(filepath)

    def test_column_names(self):
        self.assertEqual(self.result.dtype.names, column_names)


class TestLimited(unittest.TestCase):

    def setUp(self):
        filepath = os.path.join(data_dir, 'limited-phasespace.phsp')
        self.result = read_ntuple(filepath)

    def test_column_names(self):
        self.assertEqual(self.result.dtype.names, column_names_limited)


if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())
