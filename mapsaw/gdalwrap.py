# Copyright (c) 2010 Nick Thompson
# Licensed under the MIT license: http://www.opensource.org/licenses/mit-license.php
"""
Subprocess-based wrappers for GDAL utility programs.
The libraries used by gdalwarp and gdal_contour are
not exposed to Python so we can't do these operations
in-memory, we have to go through files.  /dev/shm may
ease the pain.
"""

import os
import math
import subprocess

from osgeo import osr, gdal, gdalconst, gdal_array
import numpy as N


def gdal_exec(cmd, args):
    #cmdline = '%s%s %s' % (gdal_prefix, cmd, ' '.join(args))
    sargs = [str(a) for a in args]
    print 'gdal %s %r' % (cmd, sargs)

    exitcode = subprocess.call(['/usr/bin/arch', '-i386', cmd] + sargs)
    if exitcode != 0:
        raise Exception('%s command failed with exit code %d' % (cmd, exitcode))


def gdalwarp(src, dst, srcgrid=None, dstgrid=None, interp=None, order=None, srcnodata=None, dstnodata=None):
    """very incomplete but more pythonic wrapper around gdalwarp.
    """

    args = [src]
    
    # always generate tiled tiff files for better random access
    args += '-of GTiff -co TILED=YES -co BLOCKXSIZE=128 -co BLOCKYSIZE=128'.split(' ')
    # note compressing at the same time as gdalwarp is a bad idea

    # SOURCE_EXTRA costs a bit more but avoids wraparound problems
    #  when warping near the prime meridian
    args += ['-wo', 'SOURCE_EXTRA=120']

    # -co NAME=VALUE   - set an output option, see tiff driver
    # -to NAME=VALUE   - set a transformer option, see GDALCreateGenImgProjTransformer2()
    # -wo NAME=VALUE   - set a warp option, see GDALWarpOptions::papszWarpOptions

    # use 100MB of memory.  if you have this too low performance will suck
    #  it should really be part of some global config not a param though.
    args += ['--config', 'GDAL_CACHEMAX', 100,
             '-wm', 100]

    # always use an alpha channel for missing values
    #args += ['-dstalpha']

    if interp is not None:
        args += ['-r', interp]
    if order is not None:
        args += ['-order', order]

    if srcnodata is not None:
        args += ['-srcnodata', srcnodata]
    if dstnodata is not None:
        args += ['-dstnodata', dstnodata]

    if srcgrid is not None:
        args += ['-s_srs', srcgrid.srs()]

    if dstgrid is not None:
        args += ['-t_srs', dstgrid.srs()]
        args += ['-te' ] + list(dstgrid.extent())

        # -tr is also provided by gdalwarp but -te gives same constraint

        if dstgrid.shape is not None:
            sy,sx = dstgrid.shape
            args += ['-ts', sx, sy]

        # -ot type

    args += [dst]

    return gdal_exec('gdalwarp', args)



def gdal_contour(infn, outfn, interval=100, offset=0, column=None):
    args = [infn, '-i', str(interval)]
    if offset != 0:
        args += ['-off', str(offset)]
    if column is not None:
        args += ['-a', column]
    args += [outfn]
    return gdal_exec('gdal_contour', args)
