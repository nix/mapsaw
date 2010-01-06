

.contours[sig>0] height_ft {
  text-face-name: 'DejaVu Sans Book';
  text-placement: line;
  text-max-char-angle-delta: 35;
  text-size:10;
  text-halo-radius: 0;

  text-min-distance: 200;
  text-fill: #530;
}

.osm_line name {
   text-placement: line;
   text-max-char-angle-delta: 35;
   text-size:10;
   text-min-distance: 200;
}

.osm_line[waterway='stream'] name {
   text-face-name: 'DejaVu Sans Oblique';
   text-dy: 8;
   text-fill: #36d;
}
.osm_line[waterway='creek'] name {
   text-face-name: 'DejaVu Sans Oblique';
   text-dy: 8;
   text-fill: #36d;
}
.osm_line[waterway='river'] name {
   text-face-name: 'DejaVu Sans Oblique';
   text-dy: 8;
   text-fill: #36d;
}
.osm_line[waterway='canal'] name {
   text-face-name: 'DejaVu Sans Oblique';
   text-dy: 8;
   text-fill: #36d;
}

/*
.osm_line[waterway='dam'] name {
}
.osm_line[waterway='spillway'] name {
}
.osm_line[waterway='drain'] name {
}
.osm_line[waterway='ditch'] name {
}
.osm_line[waterway='weir'] name {
}
.osm_line[waterway='riverbank'] name {
}
.osm_line[waterway='stream'] name {
}
.osm_line[waterway='spillway'] name {
}
.osm_line[waterway='creek'] name {
}
.osm_line[waterway='drain'] name {
}
.osm_line[waterway='river'] name {
}
.osm_line[waterway='canal'] name {
}
.osm_line[waterway='pipe'] name {
}
*/



.osm_line[highway='primary'] {
   text-face-name: 'DejaVu Sans Book';
   text-fill: #000;
   text-size:10;
}
.osm_line[highway='secondary'] {
   text-face-name: 'DejaVu Sans Book';
   text-fill: #000;
   text-size:10;
}
.osm_line[highway='residential'] {
   text-face-name: 'DejaVu Sans Book';
   text-fill: #000;
   text-size:10;
}
.osm_line[highway='service'] {
   text-face-name: 'DejaVu Sans Book';
   text-fill: #000;
   text-size:10;
}
.osm_line[highway='track'] {
   text-face-name: 'DejaVu Sans Book';
   text-fill: #000;
   text-size:10;
}
.osm_line[highway='cycleway'] {
   text-face-name: 'DejaVu Sans Book';
   text-fill: #000;
   text-size:10;
}
.osm_line[highway='bridleway'] {
   text-face-name: 'DejaVu Sans Book';
   text-fill: #000;
   text-size:10;
}
.osm_line[highway='footway'] {
   text-face-name: 'DejaVu Sans Book';
   text-fill: #000;
   text-size:10;
}
.osm_line[highway='path'] {
   text-face-name: 'DejaVu Sans Book';
   text-fill: #000;
   text-size:10;
}
.osm_line[highway='unclassified'] {
   text-face-name: 'DejaVu Sans Book';
   text-fill: #000;
   text-size:10;
}


/*
 nhd_points.ftype in Well SpringSeep Waterfall Rapids Rock
 nhdflowline.ftype in StreamRiver CanalDitch ArtificialPath Coastline Connector Pipeline      
*/

.nhd_waterbody gnis_name {
   text-face-name: 'DejaVu Sans Book';
   text-max-char-angle-delta: 35;
   text-size:10;
   text-min-distance: 200;
   text-fill: #009;
   text-placement: point;
}

/*
.nhd_waterbody ftype {
   text-face-name: 'DejaVu Sans Book';
   text-max-char-angle-delta: 35;
   text-dy:30;
   text-size:8;
   text-fill: black
}
*/
