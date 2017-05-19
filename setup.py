#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    "numpy"
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='topas2numpy',
    version='0.2.0',
    description="Python functions for reading TOPAS result files",
    long_description=readme + '\n\n' + history,
    author="David Hall",
    author_email='dhcrawley@gmail.com',
    url='https://github.com/davidchall/topas2numpy',
    packages=[
        'topas2numpy',
    ],
    package_dir={'topas2numpy':
                 'topas2numpy'},
    include_package_data=True,
    install_requires=requirements,
    license="MIT",
    zip_safe=False,
    keywords=[
        'topas2numpy',
        'topas',
    ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Healthcare Industry',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Scientific/Engineering :: Medical Science Apps.',
        'Topic :: Scientific/Engineering :: Physics',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
