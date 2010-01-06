# Copyright (c) 2010 Nick Thompson
# Licensed under the MIT license: http://www.opensource.org/licenses/mit-license.php

"""

constants for the Google / Yahoo / Microsoft web mapping projection:

this projection has a few critical properties which allow it to be easily
tiled for efficient panning and zooming:
 - north-south and east-west are always vertical and horizontal respectively
 - the flattened earth is square in pixel coordinates
 - transforming between the projected grid and WGS84 lon/lat is relatively simple

these imply the following not-nice properties:
 - the latitudes are consistent with WGS84, but the projection actually
   uses a sphere instead of the WGS84 ellipsoid.  not sure how exactly.
 - latitudes more than about 85.05 degrees from the equator are not represented.

there is a great explanation at:
 http://www.sharpgis.net/post/2007/07/27/The-Microsoft-Live-Maps-and-Google-Maps-projection.aspx

also interesting:
 http://www.maptiler.org/google-maps-coordinates-tile-bounds-projection/
 http://cfis.savagexi.com/articles/2006/05/03/google-maps-deconstructed
 http://cfis.savagexi.com/articles/2006/06/30/mouse-coordinates-to-lat-long

After years of stonewalling, EPSG finally issued EPSG:3785
In the meantime some folks decided to use "900919" ("google" in l33t-speak)
as a code number for this projection.
Later EPSG deprecated EPSG:3785 in favor of EPSG:3857.

"""

tilesize = 256

# See the "Virtual Earth Mercator" section at <http://proj.maptools.org/faq.html>
#  for the reasoning behind this PROJ.4 incantation.
proj4_srs = "+proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +no_defs"

# the poles are clipped off to get a square image.
# in wgs84 coords the bounds are
#        -180 -85.05112877980659    180 85.05112877980659
# in gmaps coords:
#        -20037508.3427892 -20037508.3427892     20037508.3427892 20037508.3427892
geo_left =   - 20037508.3427892
geo_bottom = - 20037508.3427892
geo_right =  20037508.3427892
geo_top =    20037508.3427892

