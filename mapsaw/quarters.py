# Copyright (c) 2010 Nick Thompson
# Licensed under the MIT license: http://www.opensource.org/licenses/mit-license.php

"""
functions for shrinking images (and joining quarters).

these are used to seed the elevation and surface for the next zoom layer up.

"""

import os
import numpy as N
try:
    import scipy.ndimage as ndimage
except ImportError:
    # you can compile just scipy.ndimage separately much more
    #  easily than some of scipy.  ndimage only depends on numpy.
    import ndimage

from mapsaw.grid import Grid
from mapsaw.rasterio import load_raster, save_raster


# downsample to prepare for the next zoom level out
def build_quarter(fn, info, data):
    """output an image at half resolution in both x and y.

    used to prepare for the next zoom level while the data is hot.
    """
    # filter and downsample.  could do this more gracefully with broadcasting?
    if len(data.shape) == 2:
        print 'QD', data.shape, data.dtype
        data = ndimage.zoom(data, 0.5)
        print 'QS', data.shape, data.dtype
    elif len(data.shape) == 3:
        print 'QD', data.shape, data.dtype
        outshape = (data.shape[0]/2, data.shape[1]/2, data.shape[2])
        data = N.dstack([ndimage.zoom(data[:,:,ci], 0.5)
                         for ci in range(data.shape[2])])
        print 'QS', data.shape, data.dtype

    # should this be a convenience function in Grid?
    # double the scale of pixels in the output
    geoxf = [] + info.grid.geoxf()
    for i in (1, 2, 4, 5):
        geoxf[i] *= 2
    qgrid = Grid(info.grid.srs(), geoxf=geoxf, shape=data.shape)

    save_raster(fn, data, {'grid': qgrid })


# this might be easier by creating a .vrt file?
def load_quarters(fns):
    """join four quadrants downsampled from the previous (larger) zoom level.

    this has better locality and requires less warping than extracting from
    the source data repeatedly at different zooms.

    the quadrants have overlap for processing reasons, these need to
    be removed in the middle +

    the only problem is that the margin for each zoom level decreases
    by a factor of two, but we don't want to start with a huge margin at the
    largest zoom.  so at some point we have to go into neighboring quarters.
    """
    (swinfo,sw),(seinfo,se),(nwinfo,nw),(neinfo,ne) = (load_raster(fn) for fn in fns)

    # assume all quarters have the same projection, and compatible geoxf
    # assume that they are symmetrically arranged, so we can just use sw and ne
    _, _, ebound, nbound = swinfo.grid.extent()
    wbound, sbound, _, _ = neinfo.grid.extent()
    cx = (ebound + wbound) / 2
    cy = (nbound + sbound) / 2

    # geoxf and srs are the same as swinfo,
    # but the shape doubles

    # note assumes meters but extent() returns lat/lon

    sy,sx = swinfo.grid.shape

    print 'swshape %s' % swinfo.grid.shape

    ixmin,iymin = N.dot(neinfo.grid.inv_s, (cx, cy))
    ixmax,iymax = N.dot(swinfo.grid.inv_s, (cx, cy))

    print 'overlapped %s pixels in x' % (ixmin + sx-ixmax)
    print 'overlapped %s pixels in y' % (iymin + sy-iymax)

    big = N.vstack(N.hstack(sw[:iymax,:ixmax,:], se[:iymax,ixmin:,:]),
                   N.hstack(nw[iymin:,:ixmax,:], ne[iymin:,ixmin:,:]))
             
    print 'bigshape %s' % big.shape

    return biginfo, big
