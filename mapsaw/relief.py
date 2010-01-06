# Copyright (c) 2010 Nick Thompson
# Licensed under the MIT license: http://www.opensource.org/licenses/mit-license.php
"""

This is a fast shaded relief generator.
Written in Python, requires numpy and scipy.ndimage.

This code uses fast image processing operations to do
pseudo-lighting.

Inspired by Lars Ahlzen's TopOSM, the light and self-shadow
are broken out into two images which can be adjusted
independently.  

Similar code:
 perrygeo hillshade.cpp (standalone, in c++)
  http://www.perrygeo.net/wordpress/?p=7
 mike migurski's hillshade.py (numpy, excessive trigonometry)
  http://mike.teczno.com/img/hillshade.py

This version is built for speed.
Dynamic range is carefully preserved.
Lightsource is fixed to northwest, 45 deg above horizon.
This could be generalized without much more work.

Much inspiration is available at http://www.shadedrelief.com/
particularly:
 http://www.shadedrelief.com/shelton/index.html
 http://www.shadedrelief.com/berann/index.html

"""

from math import sqrt
import numpy as N
try:
    import scipy.ndimage as ndimage
except ImportError:
    # you can compile just scipy.ndimage separately much more
    #  easily than some of scipy.  ndimage only depends on numpy.
    import ndimage


def reliefshade(deminfo, dem, surface):

    vertical_exaggeration = 2.0
    # light_gamma < 1 brings out detail in the flats, hides it in hills facing the lightsource
    light_gamma = 0.9
    light_level = 0.5
    # shade_gamma > 1 brings out detail in darkest slopes at the expense of some gentle ones
    shade_gamma = 2.0
    shade_level = 0.5
    # imhof sez the light is golden - #fffbf4 maybe?
    # and the shade is purple - #060009 maybe?
    #lightcolor = (1.0, 0.98, 0.95)
    #shadecolor = (1.0, 0.98, 0.95)
    #shadecolor = (0.7, 0.8, 1.0)
    #lightcolor = (1.0, 1.0, 1.0)
    lightcolor = (1.0, 1.0, 0.9)
    shadecolor = (1.0, 1.0, 1.0)
    #shadecolor = (0.8, 0.8, 1.0)

    # scale adjusts for horizontal and vertical units as well as
    # any height exaggeration.
    scale = vertical_exaggeration / deminfo.grid.meters_per_grid()

    # 2d prewitt filter kernel with axis=1 is [[-1, 0, 1]
    #                                          [-1, 0, 1]
    #                                          [-1, 0, 1]]
    dvdx = scale * ndimage.prewitt(dem, axis=1, mode='nearest')
    dvdy = -scale * ndimage.prewitt(dem, axis=0, mode='nearest')

    #glumpy_loop(N.outer(dvdx, (1,1,1)).reshape(surface.shape))

    # the idea of separating light and shadow is from lars
    #  ahlzen's toposm work, this is slightly different.

    # normal vector is (-dvdx, -dvdy, 1)
    #  norm of normal is sqrt(dvdx * dvdx + dvdy * dvdy + 1)
    # vector toward light is (-1, 1, 1)
    #  norm of light vector sqrt(3)
    norm = N.sqrt(3 * (dvdx * dvdx + dvdy * dvdy + 1))
    
    # light_dir = (-1, 1, 1)
    # cos(theta) = light_dir . normal / |normal| |light_dir|
    #
    costh = (dvdx - dvdy + 1) / norm

    # separate into illumination and (self-)shadow

    # costh_level is costh for a horizontal surface.  anything brighter
    #  than this is light, anything darker is shade.
    # this is (light=0,shade=1)
    costh_level = 1.0 / sqrt(3)

    # the minimum possible costh is for a cliff facing southwest
    #  which would have dvdx=-BIG and dvdy=+BIG.  plug that into
    #  the costh formula and you get -sqrt(2/3)
    # this is the darkest possible shade (light=0,shade=0)
    costh_min = -sqrt(2.0 / 3.0)

    # light is 1.0 for a surface pointing sunward and 0.0 at horizontal
    light = N.clip((costh - costh_level) / (1 - costh_level), 0, 1)
    light = light ** (1/light_gamma)

    # shade is 1.0 for horizontal and 0.0 for a vertical cliff facing
    #   away from the lightsource.
    # note that shade=0 is still darkest, 1 is lightest
    shade = N.clip((costh-costh_min) / (costh_level-costh_min), 0, 1)
    shade = shade ** (1/shade_gamma)

    # this would be a great place for a "tone mapping" like step
    # to adapt the relief to meadows or mountains.

    #  N.outer flattens so must reshape to rgb afterward
    light = N.outer(light, lightcolor).reshape(surface.shape)
    shade = N.outer(shade, shadecolor).reshape(surface.shape)

    # moderate the effect of light and shade here
    light = light * light_level
    shade = shade * shade_level + (1 - shade_level)

    # light brings the surface closer to the light color
    #  XXX the white highlights look like plastic, mix in
    #  the surface color a bit more?
    lit = (1 - (1-surface) * (1-light))

    # shade darkens to black anywhere
    relief = lit * shade

    return relief

