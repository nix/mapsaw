# Copyright (c) 2010 Nick Thompson
# Licensed under the MIT license: http://www.opensource.org/licenses/mit-license.php

"""

Customizable code to copy data from one OGR datasource to another.
Right now both input and output must be shapefiles.
The base class functions like ogr2ogr.py.

The idea of OgrFilter is that you subclass it to make changes to the data.

"""

import os, sys
from osgeo import ogr, osr
from mapsaw.util import attrdict

shp_drv = ogr.GetDriverByName( 'ESRI Shapefile' )

def features(layer):
    """note that features are destroyed after each yield.
    this should only be used in filters
    """
    feat = layer.GetNextFeature()
    while feat is not None:
        yield feat

        feat.Destroy()
        feat = layer.GetNextFeature()


def ogr_info(ds):
    layers = [attrdict(name=defn.GetName(),
                       geom_type=defn.GetGeomType(),
                       srs=srclayer.GetSpatialRef().ExportToProj4(),
                       fields=[attrdict(name=field.GetName(),
                                        type=field.GetType(),
                                        width=field.GetWidth(),
                                        precision=field.GetPrecision())
                               for field in (defn.GetFieldDefn(i)
                                             for i in range(defn.GetFieldCount()))])
              for defn,srclayer in ((l.GetLayerDefn(), l)
                                    for l in map(ds.GetLayer, range(ds.GetLayerCount())))]

    return attrdict(layers=layers)


def ogr_create_schema(ds, info):
    newlayers = []
    for layer_info in info.layers:
        srs = osr.SpatialReference()
        srs.ImportFromProj4(layer_info.srs)

        layer = ds.CreateLayer(layer_info.name,
                               srs=srs,
                               geom_type=layer_info.geom_type)

        for fieldinfo in layer_info.fields:
            fd = ogr.FieldDefn(fieldinfo.name, fieldinfo.type)
            fd.SetWidth(fieldinfo.width)
            fd.SetPrecision(fieldinfo.precision)
            layer.CreateField(fd)

        newlayers.append(layer)
    return newlayers


class OgrFilter(object):
    # XXX note can't add or delete layers here because of fragile code below
    def edit_schema(self, info):
        """SUBCLASS HOOK
        """
        return info

    def edit_feature(self, feat, layer_info):
        """SUBCLASS HOOK
        """
        return feat

    def filter(self, infile, outfile):
        """Run the filter.

        Infile is an existing shapefile.  Outfile is a new shapefile.
        """
        print infile, outfile

        inshp = ogr.Open(infile, update=0)
        assert inshp is not None

        #shp_drv.DeleteDataSource(outfile)
        outshp = shp_drv.CreateDataSource(outfile)
        assert outshp is not None

        info = ogr_info(inshp)
        info = self.edit_schema(info)

        ogr_create_schema(outshp, info)
        srclayers = map(inshp.GetLayer, range(inshp.GetLayerCount()))
        dstlayers = map(outshp.GetLayer, range(outshp.GetLayerCount()))
        for i, layer_info in enumerate(info.layers):
            self._copy_layer(srclayers[i], layer_info, dstlayers[i])

        outshp.Destroy()
        inshp.Destroy()

    def _copy_layer(self, srclayer, layer_info, dstlayer):
        """Copy an OGR layer.
        """

        for feat in features(srclayer):
            f = attrdict(feat.items())
            # grab geometry too?

            f = self.edit_feature(f, layer_info)
            if f is None:
                continue

            outf = ogr.Feature(feature_def=dstlayer.GetLayerDefn())
            for k, v in f.items():
                outf.SetField(k, v)
            outf.SetGeometry(feat.GetGeometryRef())
            #outf.SetFrom(feat)
            dstlayer.CreateFeature(outf)
            outf.Destroy()

if __name__ == '__main__':
    filt = OgrFilter()
    filt.filter(sys.argv[1], sys.argv[2])
