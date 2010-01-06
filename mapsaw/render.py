# Copyright (c) 2010 Nick Thompson
# Licensed under the MIT license: http://www.opensource.org/licenses/mit-license.php
"""

use cascadenik and mapnik to render a set of vectors to a numpy array.

"""

import os
import numpy as N

import mapnik

from mapsaw.util import attrdict
from mapsaw import mapconfig

# use pkg_resources to find mss files for now anyway
from pkg_resources import resource_string

def get_mss(name):
    """look up the cascadenik stylesheet for a map using pkg_resources
    """
    mssfile = 'topostyle/%s.mss' % name
    return resource_string(__name__, mssfile)


def get_rulegroups(decls, dir):
    from cascadenik.compile import get_polygon_rules, get_polygon_pattern_rules, get_line_rules, get_line_pattern_rules, get_shield_rule_groups, get_text_rule_groups, get_point_rules

    yield ('polygon', get_polygon_rules(decls))
    yield ('polygon pattern', get_polygon_pattern_rules(decls, dir))
    yield ('line', get_line_rules(decls))
    yield ('line pattern', get_line_pattern_rules(decls, dir))

    for (name, rules) in get_shield_rule_groups(decls, dir).items():
        yield ('shield(%s)' % name, rules)

    for (name, rules) in get_text_rule_groups(decls).items():
        yield ('text(%s)' % name, rules)

    yield ('point', get_point_rules(decls, dir))



def do_mss(layers, msstxt, local_base, srs):
    from cascadenik.style import stylesheet_declarations
    from cascadenik.compile import is_gym_projection
    from cascadenik import output
    ids = (i for i in xrange(1, 999999))

    alldecls = stylesheet_declarations(msstxt, base=local_base,
                                       is_gym=is_gym_projection({'srs':srs}))

    #print 'ALL', alldecls

    olayers = []
    for layer in layers:
        # this is get_applicable_declarations
        layer_decls = [dec for dec in alldecls
                       if dec.selector.matches('Layer', None, [layer.name])]

        rule_groups = get_rulegroups(layer_decls, mapconfig.style_dir)

        styles = [output.Style('%s style %d' % (t,ids.next()), rules)
                  for t, rules in rule_groups
                  if rules]

        if styles:
            datasource = output.Datasource(**layer.datasource_params)
            olayers.append(output.Layer('layer %d' % ids.next(),
                                        datasource, styles,
                                        layer.srs,
                                        None, None))

    map_attrs = {}
    for dec in alldecls:
        if not dec.selector.matches('Map', None, []):
            continue
        if dec.property.name == 'map-bgcolor':
            map_attrs['bgcolor'] = dec.value.value

    return output.Map(srs, olayers, **map_attrs)


# XXX should rename to "render_geometry" or something
#  since it can render from a postgis db.  generalize "file" arg to "source"
def render_layer(workdir, layername, grid, sourcenames):
    layers = []
    for name in sourcenames:
        source = dict(mapconfig.datasources[name])
        if 'table' in source:
            source.update(mapconfig.db)
        if 'file' in source:
            source['type'] = 'shape'
            source['file'] = os.path.join(workdir, source['file'])

        layer = attrdict(name=name,
                         datasource_params=source)
        if 'srs' in source:
            layer.srs = source['srs']
        layers.append(layer)

    """
    if isinstance(source, basestring):
        source = dict(type='shape', file=source)
    else:
        table,multi = source
        source = dict(type='postgis',
                      table=table,
                      multiple_geometries=multi,
                      #estimate_extent='false',
                      #extent=','.join([str(x) for x in grid.extent()]),
                      user='nix',
                      dbname='osmdb')
    lines = attrdict(name='lines',
                     datasource_params=source,
                     srs=data_srs)
    """

    sy,sx = grid.shape
    srs = grid.srs()

    base = None
    styletxt = get_mss(layername)
    styles = do_mss(layers, styletxt, base, srs)

    map = mapnik.Map(sx, sy, srs)
    styles.to_mapnik(map)

    x0,y0,x1,y1 = grid.extent()

    daspect = (x1-x0) / (y1-y0) * sy / sx
    if abs(daspect - 1) > 1e-5:
        raise Exception('aspect ratios must match to avoid mapnik bug? (grid %s vs map %s)'
                        % ((x1-x0) / (y1-y0), sy / sx))

    map.zoom_to_box(mapnik.Envelope(*grid.extent()))

    if 1:
        # XXX should use a tempfile here
        mapfile = 'foo.xml'
        mapnik.save_map(map, mapfile)
        print 'MAPXML'
        print open(mapfile).read()

    img = mapnik.Image(map.width, map.height)
    mapnik.render(map, img)

    imgdata = N.frombuffer(img.tostring(), dtype=N.uint8).reshape((sy, sx, 4))
    return N.array(imgdata, N.float32) / 255.0

