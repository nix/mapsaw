# Copyright (c) 2010 Nick Thompson
# Licensed under the MIT license: http://www.opensource.org/licenses/mit-license.php
"""
Georeferenced raster I/O courtesy of the GDAL library.
"""

import os
from osgeo import osr, gdal, gdalconst, gdal_array
import numpy as N
from mapsaw.util import attrdict
from mapsaw.grid import Grid

def load_raster(input):
    """open a GDAL-readable raster file
    returns a pair of (metadata,array)
    """
    dem = gdal.Open(input)

    nodata = []
    layers = []
    for i in range(1, dem.RasterCount+1):
        band = dem.GetRasterBand(i)
        data = band.ReadAsArray(0, 0, dem.RasterXSize, dem.RasterYSize)
        layers.append(data)
        nodata.append(band.GetNoDataValue())

    if len(layers) > 1:
        layers = N.dstack(layers) 

    info = attrdict(
        metadata=dem.GetMetadata_Dict(),
        grid=Grid.from_gdal(dem),
        nodata=nodata)

    return (info,layers)


def save_raster(outfile, data, info=None):
    """open a GDAL-readable raster file
    returns a pair of (metadata,array)
    """

    proj4txt = (info and info['grid'].srs())
    geoxf = (info and info['grid'].geoxf())
    meta = None  # XXX fixme

    dirname,fname = os.path.split(os.path.abspath(outfile))
    if not os.path.isdir(dirname):
        os.makedirs(dirname)

    if len(data.shape) == 3:
        ysize,xsize,nbands = data.shape
    else:
        ysize,xsize = data.shape
        nbands = 1

    # get the gdal datatype from the numpy datatype
    gdtype = gdal_array.flip_code(data.dtype.type)

    # do not add COMPRESS=DEFLATE here
    # generate all TIFFs in blocks for faster random access
    blocksize = 128
    opts = [
        'TILED=YES',
        'BLOCKXSIZE=%d' % blocksize,
        'BLOCKYSIZE=%d' % blocksize
        ]

    #print 'SAVE %r %r' % (outfile, (data.shape, blocksize, opts))

    gtiff = gdal.GetDriverByName('GTiff')

    #print 'GDTY %r %r %r' % (data.dtype, gdtype, gdalconst.GDT_Byte)

    ds = gtiff.Create(str(outfile), xsize, ysize, nbands,
                      gdtype, opts)

    if proj4txt is not None:
        srs = osr.SpatialReference()
        srs.ImportFromProj4(proj4txt)
        ds.SetProjection(srs.ExportToWkt())

    if geoxf is not None:
        ds.SetGeoTransform(geoxf)

    if meta is not None:
        ds.SetMetadata(meta)

    for i in range(nbands):
        rband = ds.GetRasterBand(i+1)

        if nbands == 1:
            rband.SetRasterColorInterpretation(gdalconst.GCI_GrayIndex)
        elif i == 0:
            rband.SetRasterColorInterpretation(gdalconst.GCI_RedBand)
        elif i == 1:
            rband.SetRasterColorInterpretation(gdalconst.GCI_GreenBand)
        elif i == 2:
            rband.SetRasterColorInterpretation(gdalconst.GCI_BlueBand)
        elif i == 3:
            rband.SetRasterColorInterpretation(gdalconst.GCI_AlphaBand)

        #rband.SetNoDataValue(xxx):

        bdata = data
        if nbands > 1:
            bdata = data[:,:,i]

        # transform data to unsigned byte?
        print 'DATA %r: %f < x < %f' % (outfile, N.min(bdata), N.max(bdata))

        rband.WriteArray(bdata)

