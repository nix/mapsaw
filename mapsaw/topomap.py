#!/usr/bin/env pythonw
# Copyright (c) 2010 Nick Thompson
# Licensed under the MIT license: http://www.opensource.org/licenses/mit-license.php

#
#
#  preliminary code to assemble landcover and contour info
#  into a maps supertile
#
#

import os,sys,re,math
from glob import glob
import shutil
import subprocess
from osgeo import osr, ogr, gdal, gdalconst, gdal_array
from PIL import Image

import pyproj
from pyproj import Proj
#print 'PPD', pyproj.pyproj_datadir
# added symlink so this isn't needed
# pyproj.set_datapath('/Library/Frameworks/PROJ.framework/Versions/4/Resources/proj/')

import numpy as N
try:
    import scipy.ndimage as ndimage
except ImportError:
    # you can compile just scipy.ndimage separately much more
    #  easily than some of scipy.  ndimage only depends on numpy.
    import ndimage

# quick and dirty configuration file
from mapsaw import mapconfig

from mapsaw.util import *
from mapsaw.grid import Grid
from mapsaw.gdalwrap import gdalwarp
from mapsaw.rasterio import load_raster, save_raster
from mapsaw.contour import contour_find, ContourTweaker
from mapsaw.relief import reliefshade
from mapsaw.render import render_layer

from mapsaw.mrlc import landcover_info
from mapsaw import gym

from mapsaw.view import glumpy_loop
from mapsaw.quarters import load_quarters, build_quarter

from mapsaw.tileout import ramdisk, optipng


def extract_all(workdir, grid):
    # lanczos interpolator creates artifacts in the hillshading
    # cubicspline does not, at least when upsampling
    # when downsampling there is some grid noise visible in the shading
    srcfile = mapconfig.dem_source
    dstfile = '%s/dem.tif' % (workdir,)
    if not os.path.exists(dstfile):
        gdalwarp(srcfile, dstfile, dstgrid=grid, interp='cubicspline')

    # this should do nearest neighbor interpolation only
    # check here for zone, then look up bigzone in mrlc.py

    # extract from usgs seamless server:
    srcfile = mapconfig.mrlc_source

    dstfile = '%s/mrlc.tif' % (workdir,)

    srcgrid = None    # use grid declared in mrlc .img file
    if not os.path.exists(dstfile):
        gdalwarp(srcfile, dstfile, srcgrid=srcgrid, dstgrid=grid, interp='near',
                 srcnodata=127)




def asum(back, front, amax=1.0):
    a = (front[:,:,3] / amax).reshape(front.shape[:2]+(1,))
    if back.shape[2] == 3:
        front = front[:,:,:3]
    #print 'ASUM', a.shape, back.shape, front.shape
    return (1-a) * back + a * front

def map_nhd(grid):
    """
    #nhd_proj4 = '+init=epsg:4269'
    nhd_proj4 = '+proj=latlong +ellps=GRS80 +datum=NAD83 +no_defs'

    if 1:
        imgs = [render_shapefile(('nhdflowline', 'false'),
                                 nhd_proj4, grid, get_mss('nhd_flowline')),
                render_shapefile(('nhdwaterbody', 'true'),
                                 nhd_proj4, grid, get_mss('nhd_waterbody')),
                render_shapefile(('nhdarea', 'true'),
                                 nhd_proj4, grid, get_mss('nhd_area'))]


    img = asum(imgs[0], imgs[2], 1.0)
    img = asum(img, imgs[1], 1.0)
    """

    img = render_layer(workdir, 'features', grid, ['nhd_flowline', 'nhd_waterbody', 'nhd_area', 'osm_line'])
    
    #img = 1 - N.prod([1.0 - im for im in imgs], axis=0)
    #img = N.max(imgs, axis=0)
    #img = imgs[0]

    # osm roads are imported in 900913
    if 0:
        osm = render_layer('features', grid, ['osm_line'])

    if 0:
        osm = render_shapefile(('ca_line',0),
                               gym.proj4_srs, grid,
                               get_mss('osm_label'))

    if 0:
        osm = render_shapefile(('ca_point',0), gym.proj4_srs,
                               grid, get_mss('osm_point'))

    #glumpy_loop(img+osm)
    #return img
    #return osm
    #return 0.5 * (osm + img)
    #return asum(img, osm)
    return img



def halo_mask(back, front):

    # the contour label halo hides nearby lines
    # halo is blur of label's alpha channel
    halo = ndimage.gaussian_filter(front[:,:,3] / 255.0, 2.0)

    # exaggerate any opacity greater than zero
    # "brighten" the halo and invert it to create a mask
    # the * 5000 was arrived at by trial and error.  basically
    # we want slight fuzzy edges on the halo but the interior
    # should be 1.0 to completely knock out the contour line.
    mask = N.clip(1.0 - halo * 10000, 0, 1)

    # cut label halo from contour image
    return back * mask.reshape(mask.shape+(1,))



def load_mrlc(f):
    # pale green background by default
    sfcinfo, surfacelayers = load_raster(f)
    surface = surfacelayers[0]

    # nearest-neighbor upsampling creates chunky pixels - smooth
    #  the edges with a median filter since we're in index space.
    # doing this in the index space keeps sharp edges on the
    # landcover areas, but rounded rather than blocky.
    # compare image resolution to 30m.
    # mrlc is actually 1 arcsecond but 30m is close enough
    # for choosing a filter parameter.
    scale = 30.0 / sfcinfo.grid.meters_per_grid()
    do_median = 1
    if do_median and scale > 2.0:
        # kernel size, an odd number that is near the diameter of an mrlc cell in the image grid
        ksize = 2 * int(scale / 2) + 1
        if ksize > 21:
            # arbitrary limit so we can scale up without blowing up
            ksize = 21
        surface = ndimage.median_filter(surface, size=(ksize,ksize))

    # build the colormap
    cmap = N.zeros((256,3), N.float32)
    for code,info in landcover_info.iteritems():
        cmap[int(code),:] = [int(cc,16)
                             for cc in re.match('#(..)(..)(..)',
                                                info['natural']).groups()]

    # apply the colormap and transform to 0..1
    surface = cmap[surface] / 255.0

    return sfcinfo, surface

#
#  incomplete
#
bigtile_ntiles = 8
def do_bigtile(grid, data, zoom, ix, iy):
    """
    zoom specifies the resolution - ix and iy refer to 
    """

    # find first covered tile index at this zoom level
    # tile rows
    # tiles
    
    for iy in range(bigtile_ntiles):
        for ix in range(bigtile_ntiles):
            fn = '%d-%x-%x.png' % (zoom, ix, iy)
            

def doit(workdir, grid):
    extract_all(workdir, grid)

    # create surface 
    lcf = '%s/mrlc' % (workdir,)
    if os.path.exists(lcf + '.tif'):
        sfcinfo, surface = load_mrlc(lcf + '.tif')
    else:
        sfcinfo, surface = load_quarters(lcf)
    #print 'SFCI', sfcinfo

    # get the hydrography
    #water = map_nhd(sfcinfo.grid)
    #print 'WWWWS', water.shape
    #glumpy_loop(water)

    demf = '%s/dem' % (workdir,)
    demtif = demf + '.tif'
    if os.path.exists(demtif):
        deminfo, demlayers = load_raster(demtif)
    else:
        deminfo, demlayers = load_quarters(lcf)
    dem = demlayers[0]
    # XXX handle missing values

    #glumpy_loop(surface)

    shaded = reliefshade(deminfo, dem, surface)

    #glumpy_loop(shaded)

    # test of grid tiling
    #for (z,ix,iy) in sfcinfo.grid.itertiles():
    #    print 'TILE %d %d %d' % (z, ix, iy)
    #print 'TIFF_HISTO', N.histogram(img, new=True)

    # if we don't have the DEM in a file (because we just composited it from quadrants),
    #  save it to a file so it can be fed to gdal_contour
    if not os.path.exists(demtif):
        save_raster(deminfo, demtif, dem)

    if not os.path.isdir('%s/contour' % workdir):
        contour_find(demtif, '%s/contour' % workdir)

    if not os.path.isdir('%s/contourft' % (workdir,)):
        ContourTweaker().filter('%s/contour' % (workdir,), '%s/contourft' % (workdir,))

    feats = render_layer(workdir, 'features', grid, ['nhd_flowline', 'nhd_waterbody', 'nhd_area', 'osm_line', 'contours'])

    fills = render_layer(workdir, 'fills', grid, ['contours', 'nhd_flowline', 'nhd_waterbody', 'nhd_area', 'osm_line'])

    labels = render_layer(workdir, 'labels', grid, ['contours', 'nhd_flowline', 'nhd_waterbody', 'nhd_area', 'osm_line'])

    # add contour labels and features
    img = asum(shaded, halo_mask(feats, labels))
    img = asum(img, fills)
    img = asum(img, labels)

    # build half-resolution versions for next zoom level
    #if not os.path.isdir('%s/quarter' % (workdir,)):
    #    os.mkdir('%s/quarter' % (workdir,))
    # XXX doesn't do anything right now
    parentgrid = sfcinfo.grid

    # XXX need to figure these out based on ix%2, iy%2 at some zoom?
    is_east = 0
    is_north = 0

    quadrant = [['sw', 'se'], ['nw', 'ne']][is_north][is_east]

    mrlcdir = request_workdir(parentgrid, 'mrlc')
    build_quarter('%s/%s.tif' % (mrlcdir,quadrant), sfcinfo, surface)

    demdir = request_workdir(parentgrid, 'dem')
    build_quarter('%s/%s.tif' % (demdir,quadrant), deminfo, dem)

    return img

# 
def request_workdir(grid, filename=None):
    """find or create a workdir for the given grid.

    this tries to use a ramdisk for all temporary files.
    """

    # use a ramdisk
    d = ramdisk()
    workdir = os.path.join(d, 'work')

    # wipe tmpdir if found?
    if os.path.exists(workdir):
        shutil.rmtree(workdir, ignore_errors=True)

    if not os.path.isdir(workdir):
        os.makedirs(workdir)

    # save grid definition to a file?

    if filename is not None:
        return os.path.join(workdir, filename)
    else:
        return workdir


def save_tiles(workdir, destdir, zoom, grid, data, tilesize):
    """save optimized tiles.

    uses optipng to do the final copy to destdir.
    could be pipelined for speed (start saving next temporary file
    while waiting for optipng).
    """
    ntiles = grid.shape[0] / tilesize
    for iy in range(ntiles):
        for ix in range(ntiles):
            fn = 'z%dx%xy%x.png' % (zoom, ix, iy)
            tiledata = data[iy*256:(iy+1)*256, ix*256:(ix+1)*256,:]
            print 'TILE', fn, tiledata.shape
            img = Image.fromarray(N.array(tiledata*255, N.uint8), 'RGB')

            pngfn = os.path.join(workdir, 'tmp-%s' % fn)
            img.save(pngfn)
            # copy to the destination directory, via optipng
            optipng(pngfn, os.path.join(destdir,fn))
            #os.remove(pngfn)



def do_supertile(lon, lat, zoom, size, margin=128):
    """render the supertile containing lon,lat

    int zoom is the GYM tile zoom level.
    size and margin are in pixels.
    """
    tilesize = 256

    # difference in zoom between tile and supertile
    dzoom = math.log(size / tilesize, 2)

    # build a grid where each cell is a supertile at the
    # target resolution, and look up the requested location within
    # that grid.
    stgrid = Grid.gym_tiles(zoom - dzoom)
    stx, sty = stgrid.ll2i(lon, lat)

    # get a grid for all tiles at the requested zoom level
    #  that are contained in the supertile.
    tilegrid = stgrid.expand_tile(int(stx), int(sty), size/tilesize)

    # and get a grid for pixels within the supertile (this is the geoxf)
    pixelgrid = stgrid.expand_tile(int(stx), int(sty), size)

    # to handle boundary conditions, duplicate a margin around all
    # edges of the supertile.  the step that requires the largest
    # margin is probably label placement?
    workgrid = pixelgrid.with_margin(margin)

    # request a directory for temporary files
    workdir = request_workdir(workgrid)

    # extract and render the supertile
    img = doit(workdir, workgrid)

    # clip off the margin (returning to pixelgrid) and save tiles

    # destdir should not be on the ramdisk
    destdir = os.path.join(workdir, 'tiles')
    if not os.path.isdir(destdir):
        os.makedirs(destdir)

    save_tiles(workdir,
               destdir,
               zoom,
               pixelgrid, img[margin:-margin,margin:-margin,:],
               tilesize)

    # save the whole thing as a tif for debugging
    save_raster('%s/geo.tif' % (workdir,),
                N.array(img*255, N.uint8),
                attrdict(grid=workgrid))

    return img



if __name__ == '__main__':
    #
    #  MUST BE SQUARE FOR NOW!
    #

    # mt tam
    #center = (-122.62, 37.95)

    # sf
    center = (-122.42, 37.77)

    #marin headlands?
    #center = (-122.55, 37.87)

    img = do_supertile(center[0], center[1], 15, 1024)
    #img = do_supertile(center[0], center[1], 11, 2048)

    # debugging
    #glumpy_loop(img)

