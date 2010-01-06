# Copyright (c) 2010 Nick Thompson
# Licensed under the MIT license: http://www.opensource.org/licenses/mit-license.php
"""
A Grid object contains a projection and a transform.
Basically this is the same as the metadata that GDAL
associates with a raster datasource.

This class bundles up the projection and geoxf into a single
abstraction and provides convenience functions.  Actual data
can be held in a numpy array.

It should tolerate missing metadata as well as possible, i.e.
some calculations are still possible if you don't know the
projection.

There should be some built-in support for pyramids, and
eventually for padded grids for intermediate processing.
"""

import os, sys, re
from math import pi, log, tan, fmod, atan, exp, floor, ceil, sqrt
import numpy as N

from osgeo import osr
import pyproj
from pyproj import Proj

from mapsaw import gym

wgs84 = Proj(init='epsg:4326')

def fix_geoxf(geoxf):
    if geoxf is None:
        return None,None

    geoxf = N.array(geoxf).reshape((2, 3))
    t = geoxf[:,0]
    s = geoxf[:,1:]
    return t, s

# surely there is a convenience for this somewhere?
def parse_proj4(proj4):
    d = dict((re.split('=', pair, 2)+[True])[:2] for pair in proj4.split(' +'))
    if '' in d:
        del d['']

    if 0: # not necessary in newer versions of pyproj
        if 'a' in d and 'b' in d and d['a'] == d['b'] and d['a'] == '6378137':
            if 'nadgrids' not in d:
                print 'ADDING NADGRIDS NULL'
                d['nadgrids'] = '@null'
    return d


def fix_proj(proj):
    if isinstance(proj, Proj):
        return proj
    elif isinstance(proj, basestring):
        if proj.startswith('+'):
            return Proj(proj)
        else:
            return Proj({'init':proj})
    elif isinstance(proj, osr.SpatialReference):
        proj4 = proj.ExportToProj4()
        print 'CONV', proj, proj.ExportToProj4()
        return Proj(proj4)

    raise Exception('unknown type for Grid proj parameter')


class Grid(object):
    """holds a projection and optional other stuff.

    other stuff: geoxf, shape
    iff this is a google maps tile: zoom, ix, iy  ??
    """
    def __init__(self, proj, geoxf=None, t=None, s=None, shape=None):
        """return a Grid object with the given parameters.

        most parameters are optional - it is fine to use
        the grid class just to represent a projection with
        no attached geoxf.
        """
        self.proj = fix_proj(proj)

        self.s = s
        self.t = t
        if geoxf is not None:
            self.t, self.s  = fix_geoxf(geoxf)

        if self.s is not None:
            self.s_inv = N.linalg.inv(self.s)

        self.shape = shape and N.array(shape)

    @classmethod
    def from_gdal(cls, ds):
        """return a Grid object that describes a GDAL Datasource
        """
        srs = osr.SpatialReference()
        srs.ImportFromWkt(ds.GetProjection())
        print 'DSP', srs.ExportToProj4()

        g = cls(srs,
                geoxf=ds.GetGeoTransform(),
                shape=(ds.RasterXSize, ds.RasterYSize))

        return g

    @classmethod
    def gym_pixels(cls, extent=None, shape=None, zoom=None):
        """create a grid that describes pixels of a GYM zoom level

        extent is in wgs84 lon/lat
        """
        srs = gym.proj4_srs
        #srs = '+init=EPSG:3785'
        #srs = '+init=srid:900913'

        gsx = gym.geo_right - gym.geo_left
        gsy = gym.geo_top - gym.geo_bottom

        if zoom is not None:
            worldsize = 2 ** (zoom + 8)

            shape = (worldsize, worldsize)
            t = N.array((gym.geo_left, gym.geo_bottom))
            s = N.array([[gsx/worldsize,        0],
                       [0,        gsy/worldsize]])

        else:
            shape = shape
            w,s,e,n = extent

            tgrid = cls(srs)

            # convert from lon/lat to "meters"
            w,s = tgrid.ll2en(w,s)
            e,n = tgrid.ll2en(e,n)

            sx = (e-w)/shape[1]
            sy = (n-s)/shape[0]
            print 'XXxsa', sx, sy, abs(sx/sy - 1)
            scale = max(sx, sy)
            #assert abs(sx/sy - 1) < 1e-5

            ezoom = gsx / scale
            fzoom = log(ezoom, 2) - 8
            zoom = int(fzoom+0.5)
            print 'fzoom',fzoom
            #assert abs(fzoom - zoom) < 1e-5

            # quantize sx,sy
            worldsize = 2 ** (zoom + 8)
            scale = gsx/worldsize
            
            # quantize <w,s> to the pixel grid (round down)
            w = floor((w - gym.geo_left) / scale) * scale + gym.geo_left
            s = floor((s - gym.geo_bottom) / scale) * scale + gym.geo_bottom

            t = N.array((w,s))
            s = N.array([[scale, 0],
                         [0, scale]])

        return cls(srs, t=t, s=s, shape=shape)

    @classmethod
    def gym_tiles(cls, zoom):
        """create a grid that describes the tiles of a complete GYM zoom level
        """
        return cls.gym_pixels(zoom=zoom-8)


    def expand_tile(self, ix, iy, size):
        """create a grid that describes a single tile of this level at a particular pixel size.
        """
        t = self.t + N.dot(self.s, (ix, iy))
        s = self.s / size
        return Grid(self.proj, t=t, s=s,
                    shape=(size,size))

    def with_margin(self, margin=128):
        """create a grid that is a superset of self, plus the given margin in pixels on all sides
        """
        t = self.t + N.dot(self.s, (-margin, -margin))
        print 'WWMM', self.shape
        sh = (self.shape[0] + 2*margin, self.shape[1] + 2*margin) + tuple(self.shape[2:])
        return Grid(self.proj, t=t, s=self.s, shape=sh)


    def find_zoom(self):
        """ assuming this is a google maps grid, figure out the zoom

        ??? pixels vs tiles?
        """
        #assert self.proj.srs == gym.proj4_srs, 'itertiles() requires 900913 proj, not %s' % self.proj.srs
        assert abs(self.s[0,1]) < 1e-6 and abs(self.s[1,0]) < 1e-6, 'geoxf %s contains shear' % self.s

        assert abs(abs(self.s[0,0]) - abs(self.s[1,1])) < 1e-6, 'geoxf %s contains nonuniform scale' % self.s

        # size in pixels of this zoom level
        levelsize = (gym.geo_right - gym.geo_left) / self.s[0,0]
        zoom = log(levelsize, 2) - 8

        print 'kZ', zoom, self.s

        # enable later - this checks that the grid looks like a gmaps projection
        #assert abs(zoom - int(round(zoom))) < 1e-6, 'suspicious zoom value %s' % zoom

        zoom = int(round(zoom))
        return zoom

    def itertiles(self, wsen=None):
        """generate triples (zoom, ix, iy) for all tiles overlapping an area.

        by default the area is the whole grid.
        """
        # find the gym zoom level for this grid
        zoom = self.find_zoom()
        
        # width and height of the zoom level in tiles
        level_ntiles = 2 ** zoom
        
        # by default applies to the whole grid
        if wsen is None:
            w,s = self.t
            sy,sx = self.shape
            e,n = self.t + N.dot(self.s, (sx-1, sy-1))

            # make sure that w<e and s<n
            if e < w: tmp=e ; e=w ; w=tmp
            if n < s: tmp=n ; n=s ; s=tmp

            ix0,iy0 = int(floor(self.en2i(w, s)))
            ix1,iy1 = int(ceil(self.en2i(e, n)))
        else:
            w,s,e,n = wsen
            ix0,iy0 = int(floor(self.ll2i(w, s)))
            ix1,iy1 = int(ceil(self.ll2i(e, n)))

        print 'ITER', ix0, iy0, ix1, iy1

        for iy in range(iy0, iy1):
            for ix in range(ix0, ix1):
                yield (zoom, ix, iy)

    def srs(self):
        """get the Proj.4 SRS string for the grid projection
        """
        # subs to hide some weird bugs(?) in pyproj.Proj.srs

        srs = self.proj.srs.strip()

        print 'RAW SRS %r' % (srs,)

        if 0:
            # for some reason +proj= comes back as ++proj= and
            #  +init= comes back as ++init=
            srs = re.sub(r'\+\+', '+', srs)

            # for some reason there's an extra '=True' in the middle
            #  is this the remnants of +nadgrids=@null going in?
            # +nadgrids=@null is not making the roundtrip, and
            #  it gets haphazardly  re-inserted in fix_proj above.  this is bad.
            # what's up, pyproj?
            srs = re.sub(r'\s*=True', '', srs)

        return srs

    def geoxf(self):
        """get the geographic transform as a list of length 6
        """
        return [self.t[0], self.s[0,0], self.s[0,1], 
                self.t[1], self.s[1,0], self.s[1,1]]

    def i2ll(self, ix, iy):
        """transform a point from grid ix,iy to wgs84 lon,lat
        """
        x,y = self.t + N.dot(self.s, (ix, iy))
        xy = pyproj.transform(self.proj, wgs84, x, y)
        return xy

    def i2en(self, ix, iy):
        """transform a point from grid ix,iy to wgs84 lon,lat
        """
        x,y = self.t + N.dot(self.s, (ix, iy))
        return x,y

    def en2i(self, e, n):
        """transform a point from easting,northing in meters to grid ix,iy
        """
        zoom = self.find_zoom()
        level_ntiles = 2 ** zoom
        ix = level_ntiles * (e - gym.geo_left) / (gym.geo_right - gym.geo_left)
        iy = level_ntiles * (n - gym.geo_bottom) / (gym.geo_top - gym.geo_bottom)
        return ix,iy

    def ll2en(self, lon, lat):
        """transform a point from wgs84 lon,lat to easting,northing in meters
        """
        return pyproj.transform(wgs84, self.proj, lon, lat)

    def ll2i(self, lon, lat):
        """transform a point from wgs84 lon,lat to grid ix,iy
        """
        en = self.ll2en(lon, lat)
        ixiy = N.dot(self.s_inv, en - self.t)
        return ixiy

    def meters_per_grid(self):
        """estimate the number of meters per ix/iy division
        """
        py,px = self.shape / 2
        lon0, lat0 = self.i2ll(px, py)
        oproj = Proj(proj='ortho', lat_0=lat0, lon_0=lon0)
        lon1, lat1 = self.i2ll(px+1, py+1)
        #print 'ORP', oproj(lon0, lat0), oproj(lon1, lat1)
        dp = oproj(lon1, lat1)
        scale = sqrt(N.dot(dp,dp) / 2)
        #print 'SCALE = %s m/px' % scale
        return scale

    def extent(self):
        """return (w,s,e,n) bounds for the grid in easting/northing
        """
        sy,sx = self.shape
        e0, n0 = self.i2en(0, 0)
        e1, n1 = self.i2en(sx, sy)
        if e1 < e0:
            tmp = e0
            e0 = e1
            e1 = tmp
        if n1 < n0:
            tmp = n0
            n0 = n1
            n1 = tmp
        return (e0, n0, e1, n1)

    def extentll(self):
        """return (w,s,e,n) bounds for the grid in wgs84 lon/lat
        """
        sy,sx = self.shape
        lon0, lat0 = self.i2ll(0, 0)
        lon1, lat1 = self.i2ll(sx, sy)
        if lon1 < lon0:
            tmp = lon0
            lon0 = lon1
            lon1 = tmp
        if lat1 < lat0:
            tmp = lat0
            lat0 = lat1
            lat1 = tmp
        return (lon0, lat0, lon1, lat1)

    def __str__(self):
        return '<Grid>'
