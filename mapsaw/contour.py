# Copyright (c) 2010 Nick Thompson
# Licensed under the MIT license: http://www.opensource.org/licenses/mit-license.php
"""

Contour utilities.

Mostly for doing contours in feet rather than meters.
Also adds a "significance" column which can be used to hide
some contours when they get dense.

"""

from mapsaw.ogrfilter import OgrFilter
from mapsaw.util import *
from mapsaw.gdalwrap import gdal_contour

feet_per_meter = 3.2808399
meters_per_foot = 0.3048006096012192

class ContourTweaker(OgrFilter):
    """Subclass of OgrFilter that adds "height_ft" and "sig" columns.
    """
    # XXX note can't add or delete layers here because of fragile code below
    def edit_schema(self, info):
        fields = info.layers[0].fields
        heightf, = [f for f in fields if f.name=='height']

        # copy the height field, change the name to height_ft and add it
        height_ft_f = attrdict(heightf)
        height_ft_f.name = 'height_ft'
        fields.append(height_ft_f)

        # add a "sig" field for "significance"
        sig_f = attrdict(heightf)
        sig_f.name = 'sig'
        fields.append(sig_f)

        return info

    def edit_feature(self, feat, layer_info):
        hft = int(feat.height / meters_per_foot + 0.5)
        feat.height_ft = hft

        feat.sig = 0
        if hft % 200 == 0:
            feat.sig = 1
        if hft % 1000 == 0:
            feat.sig = 2
        if hft % 5000 == 0:
            feat.sig = 3

        # add zoom level weight
        return feat

def contour_find(demfile, contourdir):
    """gdal_contour dem -> shapefile"""

    interval = 50 * meters_per_foot

    # the offset is used because otherwise contouring is between
    #   h<0 and h=0, and when water is at h=0 you don't get a shoreline
    #   as a contour.  maybe this doesn't matter with the hydrography
    #   layer working.
    # also: there are bogus elevation features in sf bay and along the shores,
    # up to 0.25m high.  so masking with hydrography may be the only option.
    gdal_contour(demfile, contourdir,
                 interval=interval,
                 offset=0.00001,
                 column='height')

