===============================
topas2numpy
===============================

|pypi| |travis-ci| |coveralls| |readthedocs|

Reading TOPAS_ results into NumPy_ arrays.



Features
--------

TOPAS_ is a Monte Carlo tool for particle simulation, designed for medical physics research. It can output two data types:

- **binned**: a quantity (e.g. dose) is accumulated within a binned geometry component
- **ntuple**: multiple data columns are recorded per particle history

This package is able to read both data types, allowing further analysis within Python.



Basic Usage
-----------

.. code-block:: python

    from topas2numpy import BinnedResult
    x = BinnedResult('Dose.csv')

    from topas2numpy import read_ntuple
    y = read_ntuple('Beam.phsp')



.. _TOPAS: http://www.topasmc.org
.. _NumPy: http://www.numpy.org


.. |pypi| image:: https://img.shields.io/pypi/v/topas2numpy.svg
        :target: https://pypi.python.org/pypi/topas2numpy
        :alt: PyPI Package

.. |travis-ci| image:: https://img.shields.io/travis/davidchall/topas2numpy.svg
        :target: https://travis-ci.org/davidchall/topas2numpy
        :alt: Build Status

.. |coveralls| image:: https://coveralls.io/repos/github/davidchall/topas2numpy/badge.svg?branch=master
        :target: https://coveralls.io/github/davidchall/topas2numpy?branch=master
        :alt: Code Coverage

.. |readthedocs| image:: http://readthedocs.org/projects/topas2numpy/badge/?version=latest
        :target: http://topas2numpy.readthedocs.org/en/latest/?badge=latest
        :alt: Documentation Status
