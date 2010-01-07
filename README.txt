
======
Mapsaw
======

Mapsaw is Python code for rendering maps.  The architecture
is intended to render one "supertile" at a time, where a
complete supertile can be rendered in main memory.

Extracting input data for the supertile(s) to be rendered
is a preprocessing step that ideally involves a single pass
over the source data.

Mapsaw is heavily inspired by Lars Ahlzen's TopOSM Colorado.
The rewrite is mostly to use more python.  No shell scripts
or imagemagick here.  Data is kept in memory as much as
possible and compositing is done with Numpy and Scipy.ndimage.
Temporary files should fit in a ramdisk.

Install
-------

Lots of prerequisites:
 Numpy
 Scipy.ndimage
 mapnik
 PIL
 GDAL (both python bindings and utility programs)
 pyproj
 optipng
... others ...

Note that scipy.ndimage can be installed easily without the rest of scipy.

Mapsaw currently uses Cascadenik for styles - it requires a
development version of cascadenik from the xmlbad branch in the
repository.  Note: if you have an existing cascadenik installation
you may not want to do this:
   svn co http://mapnik-utils.googlecode.com/svn/branches/cascadenik-xmlbad
   cd mapnik-utils

Then you need one other patch to cascadenik to get mapsaw running -
see cascadenik-xmlbad-patch.diff in this directory and apply.

Then "python setup.py install" in the mapnik-utils directory and
hopefully you're good to go.

Configuration
-------------

The "configuration file" is mapsaw/mapconfig.py which you will need
to customize for your data sources.

To run mapsaw, do
  cd mapsaw
  python setup.py develop
  python mapsaw/topomap.py

This is pre-alpha - will require persistence to compile.
