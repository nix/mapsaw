#!/usr/bin/python

# Copyright (c) 2010 Nick Thompson
# Licensed under the MIT license: http://www.opensource.org/licenses/mit-license.php

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='mapsaw',
    version='0.0.6',
    author='Nick Thompson',
    author_email='nix@nixweb.com',
    maintainer_email='nix@nixweb.com',
    license='private',
    url='http://nixweb.com',
    description='Utilities for creating maps in Python',
    long_description="""Utilities for creating maps in Python, based around
GDAL, Mapnik, Numpy, Scipy.ndimage.""",
    packages=['mapsaw'],
    scripts=[],

    # this should be some other var
    #xxx_package_xxx = {'mapsaw.data': '*.txt'},
    # cause this isnt right
    include_package_data = True,  

    install_requires=[
        'python-dateutil',
        # numpy, scipy.ndimage, mapnik, osgeo, pyproj
    ],

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console'
        ],
)
