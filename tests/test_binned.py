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
import numpy as np

# project imports
from topas2numpy import BinnedResult


data_dir = 'tests/data'
ascii_1d_path = os.path.join(data_dir, 'Dose.csv')
ascii_2d_path = os.path.join(data_dir, 'SurfaceTracks.csv')
binary_1d_path = os.path.join(data_dir, 'Dose.bin')

all_statistics = [
    'Sum', 'Mean', 'Histories_with_Scorer_Active', 'Count_in_Bin',
    'Second_Moment', 'Variance', 'Standard_Deviation', 'Min', 'Max'
]


class TestAscii1D(unittest.TestCase):
    def setUp(self):
        self.result = BinnedResult(ascii_1d_path)

    def test_quantity(self):
        assert self.result.quantity == 'DoseToWaterBinned'
        assert self.result.unit == 'Gy'

    def test_dimensions(self):
        assert len(self.result.dimensions) == 3
        assert self.result.dimensions[0].name == 'X'
        assert self.result.dimensions[1].name == 'Y'
        assert self.result.dimensions[2].name == 'Z'
        assert self.result.dimensions[0].unit == 'cm'
        assert self.result.dimensions[1].unit == 'cm'
        assert self.result.dimensions[2].unit == 'cm'
        assert self.result.dimensions[0].n_bins == 1
        assert self.result.dimensions[1].n_bins == 1
        assert self.result.dimensions[2].n_bins == 300
        assert self.result.dimensions[0].bin_width == 10.2
        assert self.result.dimensions[1].bin_width == 10.2
        assert self.result.dimensions[2].bin_width == 0.1

    def test_data(self):
        assert len(self.result.statistics) == 1
        assert self.result.statistics[0] == 'Sum'
        assert len(self.result.data) == 1
        data = self.result.data['Sum']
        assert data.dtype == np.float64
        assert data.shape[0] == self.result.dimensions[0].n_bins
        assert data.shape[1] == self.result.dimensions[1].n_bins
        assert data.shape[2] == self.result.dimensions[2].n_bins


class TestAscii2D(unittest.TestCase):
    def setUp(self):
        self.result = BinnedResult(ascii_2d_path, dtype=np.uint32)

    def test_quantity(self):
        assert self.result.quantity == 'SurfaceTrackCount'
        assert self.result.unit is None

    def test_dimensions(self):
        assert len(self.result.dimensions) == 3
        assert self.result.dimensions[0].name == 'X'
        assert self.result.dimensions[1].name == 'Y'
        assert self.result.dimensions[2].name == 'Z'
        assert self.result.dimensions[0].unit == 'cm'
        assert self.result.dimensions[1].unit == 'cm'
        assert self.result.dimensions[2].unit == 'cm'
        assert self.result.dimensions[0].n_bins == 10
        assert self.result.dimensions[1].n_bins == 10
        assert self.result.dimensions[2].n_bins == 1
        assert self.result.dimensions[0].bin_width == 6
        assert self.result.dimensions[1].bin_width == 6
        assert self.result.dimensions[2].bin_width == 60

    def test_data(self):
        assert len(self.result.statistics) == 1
        assert self.result.statistics[0] == 'Sum'
        assert len(self.result.data) == 1
        data = self.result.data['Sum']
        assert data.dtype == np.uint32
        assert data.shape[0] == self.result.dimensions[0].n_bins
        assert data.shape[1] == self.result.dimensions[1].n_bins
        assert data.shape[2] == self.result.dimensions[2].n_bins


class TestBinary1D(unittest.TestCase):
    def setUp(self):
        self.result = BinnedResult(binary_1d_path)

    def test_quantity(self):
        assert self.result.quantity == 'DoseToMedium'
        assert self.result.unit == 'Gy'

    def test_dimensions(self):
        assert len(self.result.dimensions) == 3
        assert self.result.dimensions[0].name == 'X'
        assert self.result.dimensions[1].name == 'Y'
        assert self.result.dimensions[2].name == 'Z'
        assert self.result.dimensions[0].unit == 'cm'
        assert self.result.dimensions[1].unit == 'cm'
        assert self.result.dimensions[2].unit == 'cm'
        assert self.result.dimensions[0].n_bins == 1
        assert self.result.dimensions[1].n_bins == 1
        assert self.result.dimensions[2].n_bins == 40
        assert self.result.dimensions[0].bin_width == 50
        assert self.result.dimensions[1].bin_width == 50
        assert self.result.dimensions[2].bin_width == 0.5

    def test_data(self):
        assert len(self.result.statistics) == len(all_statistics)
        assert self.result.statistics == all_statistics
        assert len(self.result.data) == len(all_statistics)
        data = self.result.data['Sum']
        assert data.shape[0] == self.result.dimensions[0].n_bins
        assert data.shape[1] == self.result.dimensions[1].n_bins
        assert data.shape[2] == self.result.dimensions[2].n_bins


if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())
