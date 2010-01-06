

.osm_line {
   line-join: round;
   line-cap: round;
   outline-join: round;
   outline-cap: round;
}

/*
.osm_line[waterway!=''] {
   line-color: #44f;
   line-width: 2.0;
}

.osm_line[waterway!=''] name {
   text-fill: #44f;
   text-face-name: 'DejaVu Sans Oblique';
   text-placement: line;
   text-dy: 8;
   text-max-char-angle-delta: 35;
   text-size:10;
   text-min-distance: 200;
}

.osm_line[highway=''][waterway=''] {
   line-color: #ff0;
   line-width: 10.0;
   line-join: round;
   line-cap: round;
}

 */

.osm_line[highway='primary'] {
   line-color: #aaa;
   line-width: 10;
}
.osm_line[highway='secondary'] {
   line-color: #aaa;
   line-width: 8;
}
.osm_line[highway='tertiary'] {
   line-color: #aaa;
   line-width: 6;
}
.osm_line[highway='residential'] {
   line-color: #aaa;
   line-width: 6;
}
.osm_line[highway='service'] {
   line-color: #aaa;
   line-width: 5;
}
.osm_line[highway='track'] {
   line-width: 3;
   line-color: #ddd;
}
.osm_line[highway='cycleway'] {
   line-width: 2;
   line-color: #ddd;
}

/* these might have a fill at sufficiently high zoom level? 
.osm_line[highway='bridleway'] {
   line-width: 2;
   line-color: #000;
   line-dasharray: 6,6;
}
.osm_line[highway='footway'] {
   line-width: 2;
   line-color: #000;
   line-dasharray: 6,6;
}
.osm_line[highway='path'] {
   line-width: 1.5;
   line-color: #000;
   line-dasharray: 4,4;
}
.osm_line[highway='unclassified'] {
   line-width: 3;
   line-color: #fff;
   outline-color: #d33;
   outline-width: 2;
   outline-dasharray: 6,6;
   outline-cap: butt;
}

*/



/*  nhdwaterbody.ftype in LakePond Reservoir SwampMarsh Playa Ice Mass */
.nhd_waterbody {
   polygon-fill: #bdf;
}
/*  nhdarea.ftype in StreamRiver Inundation Area Wash CanalDitch
                 SeaOcean Rapids Submerged Stream
                 Area to be Submerged, Spillway, Foreshore  */
.nhd_area {
   polygon-fill: #bdf;
}

