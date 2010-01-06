
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

Mapsaw currently uses Cascadenik for styles - it requires a
development version of cascadenik from the xmlbad branch in the
repository.  Note: if you have an existing cascadenik installation
you may not want to do this:
   svn co http://mapnik-utils.googlecode.com/svn/branches/cascadenik-xmlbad
   cd mapnik-utils
   python setup.py install

Cascadenik has some issues - it looks much nicer than the Mapnik
XML styles, but the CSS/HTML model is a bad fit with Mapnik rendering.



