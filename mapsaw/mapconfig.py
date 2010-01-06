
# quick and dirty configuration file


# downloaded from seamless.usgs.gov
dem_source = '/biggis/heredata/sfned/37n123.5w_38n122.125w/09358654.tif'

# downloaded from seamless.usgs.gov
mrlc_source = '/biggis/sfmrlc/37n123.5w_38n122.125w/57439242.tif'
# shapefile index to regional downloads:
#  /xtra/basedata/mrlc/landcover_bndry_030607_shp/landcover_bndry_030607.shp
# regional download for california+
#mrlc_src = '/xtra/basedata/mrlc/data/landcover2_3k_022007.img'


#srcfile= '/biggis/nhdplus/NHDPlus18/Hydrography/nhdflowline.shp'
nhd_source = '/biggis/nhdplus'

# this is used for url() references in stylesheets?
# what about local_base argument to do_mss?
style_dir = '.'

# only one database for now
db = dict(type='postgis',
          user='nix',
          dbname='osmdb')

nhd_proj4 = '+proj=latlong +ellps=GRS80 +datum=NAD83 +no_defs'
gym_proj4 = "+proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +no_defs"

datasources = {
    'contours': {
        'srs': gym_proj4,
        'file': 'contourft/contour.shp'
    },
    'osm_line': {
        'srs': gym_proj4,
        'table': 'ca_line'
    },
    'osm_point': {
        'srs': gym_proj4,
        'table': 'ca_point'
    },
    'nhd_flowline': {
        'srs': nhd_proj4,
        'multiple_geometries': 'false',
        'table': 'nhdflowline'
    },
    'nhd_waterbody': {
        'srs': nhd_proj4,
        'multiple_geometries': 'true',
        'table': 'nhdwaterbody'
    },
    'nhd_area': {
        'srs': nhd_proj4,
        'multiple_geometries': 'true',
        'table': 'nhdarea'
    },
}


# set to 0 to skip optipng completely
optipng_level = 2
