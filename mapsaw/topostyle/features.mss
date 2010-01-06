
.contours[sig=0] {
  line-color: #530;
  line-join: round;
  line-cap: round;
  line-width: 0.3;
}

.contours[sig>0] {
  line-color: #530;
  line-join: round;
  line-cap: round;
  line-width: 0.6;
}

/* OSM seems to have more detailed stream info than nhdplus,
 * at least in some places.  for now stick to NHD */
.nhd_flowline {
   line-color: #36d;
   line-width: 2.0;
   line-join: round;
   line-cap: round;
}

/* casing for nhd areas (which are in fill layer) */
/*  nhdwaterbody.ftype in LakePond Reservoir SwampMarsh Playa Ice Mass */
.nhd_waterbody {
   line-color: #36d;
   line-width: 2.0;
   line-join: round;
}
/*  nhdarea.ftype in StreamRiver Inundation Area Wash CanalDitch
                 SeaOcean Rapids Submerged Stream
                 Area to be Submerged, Spillway, Foreshore  */
.nhd_area {
   line-color: #36d;
   line-width: 2.0;
   line-join: round;
}


.osm_line {
   line-join: round;
   line-cap: round;
   outline-join: round;
   outline-cap: round;
}

.osm_line[highway='primary'] {
   line-color: #000;
   line-width: 12;
}
.osm_line[highway='secondary'] {
   line-color: #000;
   line-width: 10;
}
.osm_line[highway='tertiary'] {
   line-color: #000;
   line-width: 8;
}
.osm_line[highway='residential'] {
   line-color: #000;
   line-width: 8;
}
.osm_line[highway='service'] {
   line-color: #000;
   line-width: 6;
}
.osm_line[highway='track'] {
   line-color: #000;
   line-width: 4;
   line-dasharray: 6,6;
   line-cap: butt;
}
.osm_line[highway='cycleway'] {
   line-width: 4;
   line-color: #000;
}

.osm_line[highway='bridleway'] {
   line-width: 3;
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
   line-color: #d33;
   line-dasharray: 6,6;
}

