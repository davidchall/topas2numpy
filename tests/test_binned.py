#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_binned
----------------------------------

Tests for TOPAS binned reading.
"""

# system imports
import unittest
import os.path

# third-party imports
from numpy.testing import assert_array_almost_equal

# project imports
from topas2numpy import BinnedResult


data_dir = 'tests/data'
dose_path = os.path.join(data_dir, 'Dose.csv')
ntracks_path = os.path.join(data_dir, 'SurfaceTracks.csv')


class Test1D(unittest.TestCase):
    def setUp(self):
        self.result = BinnedResult(dose_path)

    def test_quantity(self):
        assert self.result.quantity == 'DoseToWaterBinned'

    def test_unit(self):
        assert self.result.unit == 'Gy'


if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())
