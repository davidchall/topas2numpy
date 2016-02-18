# -*- coding: utf-8 -*-

# system imports
import re
import os.path

# third party imports
import numpy as np


class BinnedDimension(object):
    """docstring for BinnedDimension"""
    def __init__(self, name, unit, n_bins, bin_width):
        self.name = name
        self.unit = unit
        self.n_bins = n_bins
        self.bin_width = bin_width

    def get_bin_centers(self):
        N = self.n_bins
        w = self.bin_width
        return np.linspace(0.5*w, (N-0.5)*w, N)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return False

    def __ne__(self, other):
        return not self.__eq__(other)


class BinnedResult(object):
    """Result file containing output of a TOPAS scorer.

    Attributes:
        quantity:   name of scored quantity
        unit:       unit of scored quantity
        statistics: list of available statistics (keys of data)
        dimensions: list of BinnedDimension objects
        data:       dict of scored data
    """
    def __init__(self, filepath):
        self.path = filepath
        _, ext = os.path.splitext(self.path)
        if ext == '.bin':
            self._read_binary()
        elif ext == '.csv':
            self._read_ascii()

    def _read_binary(self):
        """Reads data and metadata from binary format."""

        header_path = self.path + 'header'
        with open(header_path) as f_header:
            self._read_header(f_header.read())

        data = np.fromfile(self.path)

        # separate data by statistic
        data = data.reshape((len(self.statistics), -1), order='F')
        data = {stat: data[i] for i, stat in enumerate(self.statistics)}

        # reshape data according to binning
        data_shape = [dim.n_bins for dim in self.dimensions]
        data = {k: v.reshape(data_shape) for k, v in data.items()}

        self.data = data

    def _read_ascii(self):
        """Reads data and metadata from ASCII format."""

        header_str = ''
        with open(self.path) as f:
            for line in f:
                if line.startswith('#'):
                    header_str += line
        self._read_header(header_str)

        data = np.loadtxt(self.path, delimiter=',', unpack=True, ndmin=1)

        # separate data by statistic (neglecting bin columns when necessary)
        n_dim = len(self.dimensions)
        data = {stat: data[n_dim+i] for i, stat in enumerate(self.statistics)}

        # reshape data according to binning
        data_shape = [dim.n_bins for dim in self.dimensions]
        data = {k: v.reshape(data_shape) for k, v in data.items()}

        self.data = data

    def _read_header(self, header_str):
        """Reads metadata from the header."""

        # regular expressions
        re_float = '[-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?'
        re_uint = '\d+'
        re_binning = '{d} in (?P<nbins>' + re_uint + ') bin[ s] '
        re_binning += 'of (?P<binwidth>' + re_float + ') {unit}'

        # map of dimensions and units
        dim_units = {
            'X': 'cm',
            'Y': 'cm',
            'Z': 'cm',
            'R': 'cm',
            'Phi': 'deg',
            'Theta': 'deg',
        }

        # retrieve binning info
        self.dimensions = []
        for line in header_str.splitlines():

            for dim, unit in dim_units.items():
                re_tmp = re_binning.format(d=dim, unit=unit)
                regex = re.compile(re_tmp)
                match = regex.search(line)

                if match:
                    N = int(match.group('nbins'))
                    width = float(match.group('binwidth'))
                    dimension = BinnedDimension(dim, unit, N, width)
                    self.dimensions.append(dimension)

        # retrieve scored quantity info
        re_score_unit = '(?P<quant>.+) \( (?P<unit>.+) \) : (?P<stats>.+)'
        re_score_unitless = '(?P<quant>.+) : (?P<stats>.+)'
        regex_unit = re.compile(re_score_unit)
        regex_unitless = re.compile(re_score_unitless)

        for line in header_str.splitlines():

            match = regex_unit.search(line)
            if match:
                self.quantity = match.group('quant')
                self.unit = match.group('unit')
                self.statistics = match.group('stats').split()
                break

            match = regex_unitless.search(line)
            if match:
                self.quantity = match.group('quant')
                self.unit = None
                self.statistics = match.group('stats').split()
                break
