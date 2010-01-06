
#
#
#  info about MRLC, multiresolution land cover database
#
#

# the projection used in MRLC 2001 is albers equal area conic:
#  +proj=aea +lat_1=29.5 +lat_2=45.5 +lat_0=23.0 +lon_0=-96 +ellps=GRS80 +units=m

#
#  colors chosen by rough correspondences with
#    landcover types in patterson's natural palette
#  partcularly for codes 9x there is no correspondence in patterson,
#   used same as code "91" for all 9x but from the descriptions that's
#   probably wrong.
#

# for legend purposes, patterson orders these in a nice ramp:  (note these are nlcd92 codes)
#   http://www.shadedrelief.com/shelton/c.html
#  12 42 41,43 91  92 11 31,32,33  51 71 81 82,83,84 61 21,85 22,23

# code, name, defn  from http://www.mrlc.gov/nlcd_definitions.php
# natural from patterson's natural palette, modified for MRLC instead of NLCD92
landcover_info = {

    "11": { "code" : 11,
            "name": "Open Water",
            "natural": "#bcddff",
            "defn": "All areas of open water, generally with less than 25% cover of vegetation or soil." },

    "12": { "code" : 12,
            "name": "Perennial Ice/Snow",
            "natural": "#ffffff",
            "defn": "All areas characterized by a perennial cover of ice and/or snow, generally greater than 25% of total cover." },

    "21": { "code" : 21,
            "name": "Developed, Open Space",
            "natural": "#b19fb7",
            "defn": "Includes areas with a mixture of some constructed materials, but mostly vegetation in the form of lawn grasses. Impervious surfaces account for less than 20 percent of total cover. These areas most commonly include large-lot single-family housing units, parks, golf courses, and vegetation planted in developed settings for recreation, erosion control, or aesthetic purposes" },

    "22": { "code" : 22,
            "name": "Developed, Low Intensity",
            "natural": "#b19fb7",
            #"natural": "#af9db3",
            "defn": "Includes areas with a mixture of constructed materials and vegetation. Impervious surfaces account for 20-49 percent of total cover. These areas most commonly include single-family housing units." },

    "23": { "code" : 23,
            "name": "Developed, Medium Intensity",
            "natural": "#b19fb7",
            #"natural": "#af9db3",
            "defn": "Includes areas with a mixture of constructed materials and vegetation. Impervious surfaces account for 50-79 percent of the total cover. These areas most commonly include single-family housing units." },

    "24": { "code" : 24,
            "name": "Developed, High Intensity",
            "natural": "#b19fb7",
            # don't distinguish for now.  variation in this layer is so high that it's useless/distracting
            #"natural": "#66557f",
            "defn": "Includes highly developed areas where people reside or work in high numbers. Examples include apartment complexes, row houses and commercial/industrial. Impervious surfaces account for 80 to100 percent of the total cover." },

    "31": { "code" : 31,
            "name": "Barren Land (Rock/Sand/Clay)",
            "natural": "#f2ebd1",
            "defn": "Barren areas of bedrock, desert pavement, scarps, talus, slides, volcanic material, glacial debris, sand dunes, strip mines, gravel pits and other accumulations of earthen material. Generally, vegetation accounts for less than 15% of total cover." },

    "32": { "code" : 32,
            "name": "Unconsolidated Shore",
            "natural": "#f3ecd2",
            "defn": "Unconsolidated material such as silt, sand, or gravel that is subject to inundation and redistribution due to the action of water. Characterized by substrates lacking vegetation except for pioneering plants that become established during brief periods when growing conditions are favorable. Erosion and deposition by waves and currents produce a number of landforms representing this class." },

    "41": { "code" : 41,
            "name": "Deciduous Forest",
            "natural": "#9fbc9d",
            "defn": "Areas dominated by trees generally greater than 5 meters tall, and greater than 20% of total vegetation cover. More than 75 percent of the tree species shed foliage simultaneously in response to seasonal change." },

    "42": { "code" : 42,
            "name": "Evergreen Forest",
            "natural": "#76b598",
            "defn": "Areas dominated by trees generally greater than 5 meters tall, and greater than 20% of total vegetation cover. More than 75 percent of the tree species maintain their leaves all year. Canopy is never without green foliage." },

    "43": { "code" : 43,
            "name": "Mixed Forest",
            "natural": "#a0ba9d",
            "defn": "Areas dominated by trees generally greater than 5 meters tall, and greater than 20% of total vegetation cover. Neither deciduous nor evergreen species are greater than 75 percent of total tree cover." },

    "51": { "code" : 51,
            "name": "Dwarf Scrub",
            "natural": "#efdec0",
            "defn": "Alaska only areas dominated by shrubs less than 20 centimeters tall with shrub canopy typically greater than 20% of total vegetation. This type is often co-associated with grasses, sedges, herbs, and non-vascular vegetation." },

    "52": { "code" : 52,
            "name": "Shrub/Scrub",
            "natural": "#efdec0",
            "defn": "Areas dominated by shrubs; less than 5 meters tall with shrub canopy typically greater than 20% of total vegetation. This class includes true shrubs, young trees in an early successional stage or trees stunted from environmental conditions." },

    "71": { "code" : 71,
            "name": "Grassland/Herbaceous",
            "natural": "#fff5b8",
            "defn": "Areas dominated by grammanoid or herbaceous vegetation, generally greater than 80% of total vegetation. These areas are not subject to intensive management such as tilling, but can be utilized for grazing." },

    "72": { "code" : 72,
            "name": "Sedge/Herbaceous",
            "natural": "#fff5b8",
            "defn": "Alaska only areas dominated by sedges and forbs, generally greater than 80% of total vegetation. This type can occur with significant other grasses or other grass like plants, and includes sedge tundra, and sedge tussock tundra." },

    "73": { "code" : 73,
            "name": "Lichens",
            "natural": "#fff5b8",
            "defn": "Alaska only areas dominated by fruticose or foliose lichens generally greater than 80% of total vegetation." },

    "74": { "code" : 74,
            "name": "Moss",
            "natural": "#fff5b8",
            "defn": "Alaska only areas dominated by mosses, generally greater than 80% of total vegetation." },

    "81": { "code" : 81,
            "name": "Pasture/Hay",
            "natural": "#f3f5a1",
            "defn": "Areas of grasses, legumes, or grass-legume mixtures planted for livestock grazing or the production of seed or hay crops, typically on a perennial cycle. Pasture/hay vegetation accounts for greater than 20 percent of total vegetation." },

    "82": { "code" : 82,
            "name": "Cultivated Crops",
            "natural": "#e3e4aa",
            "defn": "Areas used for the production of annual crops, such as corn, soybeans, vegetables, tobacco, and cotton, and also perennial woody crops such as orchards and vineyards. Crop vegetation accounts for greater than 20 percent of total vegetation. This class also includes all land being actively tilled." },

    "90": { "code" : 90,
            "name": "Woody Wetlands",
            "natural": "#7fb498",
            "defn": "Areas where forest or shrubland vegetation accounts for greater than 20 percent of vegetative cover and the soil or substrate is periodically saturated with or covered with water." },

    "91": { "code" : 91,
            "name": "Palustrine Forested Wetland",
            "natural": "#7fb498",
            "defn": "Includes all tidal and non-tidal wetlands dominated by woody vegetation greater than or equal to 5 meters in height and all such wetlands that occur in tidal areas in which salinity due to ocean-derived salts is below 0.5 percent. Total vegetation coverage is greater than 20 percent." },

    "92": { "code" : 92,
            "name": "Palustrine Scrub/Shrub Wetland",
            "natural": "#7fb498",
            "defn": "Includes all tidal and non-tidal wetlands dominated by woody vegetation less than 5 meters in height, and all such wetlands that occur in tidal areas in which salinity due to ocean-derived salts is below 0.5 percent. Total vegetation coverage is greater than 20 percent. The species present could be true shrubs, young trees and shrubs or trees that are small or stunted due to environmental conditions." },

    "93": { "code" : 93,
            "name": "Estuarine Forested Wetland",
            "natural": "#7fb498",
            "defn": "Includes all tidal wetlands dominated by woody vegetation greater than or equal to 5 meters in height, and all such wetlands that occur in tidal areas in which salinity due to ocean-derived salts is equal to or greater than 0.5 percent. Total vegetation coverage is greater than 20 percent." },

    "94": { "code" : 94,
            "name": "Estuarine Scrub/Shrub Wetland",
            "natural": "#7fb498",
            "defn": "Includes all tidal wetlands dominated by woody vegetation less than 5 meters in height, and all such wetlands that occur in tidal areas in which salinity due to ocean-derived salts is equal to or greater than 0.5 percent. Total vegetation coverage is greater than 20 percent." },

    "95": { "code" : 95,
            "name": "Emergent Herbaceous Wetlands",
            "natural": "#7fb498",
            "defn": "Areas where perennial herbaceous vegetation accounts for greater than 80 percent of vegetative cover and the soil or substrate is periodically saturated with or covered with water." },

    "96": { "code" : 96,
            "name": "Palustrine Emergent Wetland (Persistent)",
            "natural": "#7fb498",
            "defn": "Includes all tidal and non-tidal wetlands dominated by persistent emergent vascular plants, emergent mosses or lichens, and all such wetlands that occur in tidal areas in which salinity due to ocean-derived salts is below 0.5 percent. Plants generally remain standing until the next growing season." },

    "97": { "code" : 97,
            "name": "Estuarine Emergent Wetland",
            "natural": "#7fb498",
            "defn": "Includes all tidal wetlands dominated by erect, rooted, herbaceous hydrophytes (excluding mosses and lichens) and all such wetlands that occur in tidal areas in which salinity due to ocean-derived salts is equal to or greater than 0.5 percent and that are present for most of the growing season in most years. Perennial plants usually dominate these wetlands." },

    "98": { "code" : 98,
            "name": "Palustrine Aquatic Bed",
            "natural": "#7fb498",
            "defn": "The Palustrine Aquatic Bed class includes tidal and nontidal wetlands and deepwater habitats in which salinity due to ocean-derived salts is below 0.5 percent and which are dominated by plants that grow and form a continuous cover principally on or at the surface of the water. These include algal mats, detached floating mats, and rooted vascular plant assemblages." },

    "99": { "code" : 99,
            "name": "Estuarine Aquatic Bed",
            "natural": "#7fb498",
            "defn": "Includes tidal wetlands and deepwater habitats in which salinity due to ocean-derived salts is equal to or greater than 0.5 percent and which are dominated by plants that grow and form a continuous cover principally on or at the surface of the water. These include algal mats, kelp beds, and rooted vascular plant assemblages." },
}

#
#  landcover class descriptions from http://landcover.usgs.gov/classes.php
#
#   Reference:
#     Cowardin, L.M., V. Carter, F.C. Golet, and E.T. LaRoe, 1979. Classification of Wetlands and Deepwater Habitat of the United States, Fish and Wildlife Service, U.S. Department of the Interior, Washington, D.C. 
#
#
#
landcover_info_1992 = {
  "11": {
    "nlcd": "#668cbf",
    "code": "11",
    "natural": "#bcddff",
    "defn": "all areas of open water, generally with less than 25% cover of vegetation/land cover.",
    "name": "Open Water"
  },
  "12": {
    "nlcd": "#ffffff",
    "code": "12",
    "natural": "#ffffff",
    "defn": "all areas characterized by year-long surface cover of ice and/or snow.",
    "name": "Perennial Ice/Snow"
  },
  "21": {
    "nlcd": "#fce3e3",
    "code": "21",
    "natural": "#af9db3",
    "defn": "Includes areas with a mixture of constructed materials and vegetation. Constructed materials account for 30-80 percent of the cover. Vegetation may account for 20 to 70 percent of the cover. These areas most commonly include single-family housing units. Population densities will be lower than in high intensity residential areas.",
    "name": "Low Intensity Residential"
  },
  "22": {
    "nlcd": "#f7ab9e",
    "code": "22",
    "natural": "#66557f",
    "defn": "Includes highly developed areas where people reside in high numbers. Examples include apartment complexes and row houses. Vegetation accounts for less than 20 percent of the cover. Constructed materials account for 80 to100 percent of the cover.",
    "name": "High Intensity Residential"
  },
  "23": {
    "nlcd": "#e6574d",
    "code": "23",
    "natural": "#66557f",
    "defn": "Includes infrastructure (e.g. roads, railroads, etc.) and all highly developed areas not classified as High Intensity Residential.",
    "name": "Commercial/Industrial/Transportation"
  },
  "31": {
    "nlcd": "#d1ccbf",
    "code": "31",
    "natural": "#f2ebd1",
    "defn": "Perennially barren areas of bedrock, desert pavement, scarps, talus, slides, volcanic material, glacial debris, beaches, and other accumulations of earthen material.",
    "name": "Bare Rock/Sand/Clay"
  },
  "32": {
    "nlcd": "#b0b0b0",
    "code": "32",
    "natural": "#f3ecd2",
    "defn": "Areas of extractive mining activities with significant surface expression.",
    "name": "Quarries/Strip Mines/Gravel Pits"
  },
  "33": {
    "nlcd": "#513c75",
    "code": "33",
    "natural": "#5ca882",
    "defn": "Areas of sparse vegetative cover (less than 25 percent of cover) that are dynamically changing from one land cover to another, often because of land use activities. Examples include forest clearcuts, a transition phase between forest and agricultural land, the temporary clearing of vegetation, and changes due to natural causes (e.g. fire, flood, etc.).",
    "name": "Transitional"
  },
  "41": {
    "nlcd": "#87c780",
    "code": "41",
    "natural": "#9fbc9d",
    "defn": "Areas dominated by trees where 75 percent or more of the tree species shed foliage simultaneously in response to seasonal change.",
    "name": "Deciduous Forest"
  },
  "42": {
    "nlcd": "#38824f",
    "code": "42",
    "natural": "#76b598",
    "defn": "Areas dominated by trees where 75 percent or more of the tree species `maintain their leaves all year. Canopy is never without green foliage.",
    "name": "Evergreen Forest"
  },
  "43": {
    "nlcd": "#d3e8b0",
    "code": "43",
    "natural": "#a0ba9d",
    "defn": "Areas dominated by trees where neither deciduous nor evergreen species represent more than 75 percent of the cover present.",
    "name": "Mixed Forest"
  },
  "51": {
    "nlcd": "#dbc975",
    "code": "51",
    "natural": "#efdec0",
    "defn": "Areas dominated by shrubs; shrub canopy accounts for 25-100 percent of the cover. Shrub cover is generally greater than 25 percent when tree cover is less than 25 percent. Shrub cover may be less than 25 percent in cases when the cover of other life forms (e.g. herbaceous or tree) is less than 25 percent and shrubs cover exceeds the cover of the other life forms.",
    "name": "Shrub/Scrub"
  },
  "61": {
    "nlcd": "#baad75",
    "code": "61",
    "natural": "#c8dd9c",
    "defn": "Orchards, vineyards, and other areas planted or maintained for the production of fruits, nuts, berries, or ornamentals.",
    "name": "Orchards/Vineyards/Other"
  },
  "71": {
    "nlcd": "#fce8ab",
    "code": "71",
    "natural": "#fff5b8",
    "defn": "Areas dominated by upland grasses and forbs. In rare cases, herbaceous cover is less than 25 percent, but exceeds the combined cover of the woody species present. These areas are not subject to intensive management, but they are often utilized for grazing.",
    "name": "Grasslands/Herbaceous"
  },
  "81": {
    "nlcd": "#fcf75e",
    "code": "81",
    "natural": "#f3f5a1",
    "defn": "Areas of grasses, legumes, or grass-legume mixtures planted for livestock grazing or the production of seed or hay crops.",
    "name": "Pasture/Hay"
  },
  "82": {
    "nlcd": "#c99147",
    "code": "82",
    "natural": "#e3e4aa",
    "defn": "Areas used for the production of crops, such as corn, soybeans, vegetables, tobacco, and cotton.",
    "name": "Row Crops"
  },
  "83": {
    "nlcd": "#796b49",
    "code": "83",
    "natural": "#e3e4aa",
    "defn": "Areas used for the production of graminoid crops such as wheat, barley, oats, and rice.",
    "name": "Small Grains"
  },
  "84": {
    "nlcd": "#f5edcc",
    "code": "84",
    "natural": "#e3e4ab",
    "defn": "Areas used for the production of crops that do not exhibit visable vegetation as a result of being tilled in a management practice that incorporates prescribed alternation between cropping and tillage.",
    "name": "Fallow"
  },
  "85": {
    "nlcd": "#f09c36",
    "code": "85",
    "natural": "#b19fb7",
    "defn": "Vegetation (primarily grasses) planted in developed settings for recreation, erosion control, or aesthetic purposes. Examples include parks, lawns, golf courses, airport grasses, and industrial site grasses.",
    "name": "Urban/Recreational Grasses"
  },
  "91": {
    "nlcd": "#c9e6fa",
    "code": "91",
    "natural": "#7fb498",
    "defn": "Areas where forest or shrubland vegetation accounts for 25-100 percent of the cover and the soil or substrate is periodically saturated with or covered with water.",
    "name": "Woody Wetlands"
  },
  "92": {
    "nlcd": "#91bfd9",
    "code": "92",
    "natural": "#a4ccc4",
    "defn": "Areas where perennial herbaceous vegetation accounts for 75-100 percent of the cover and the soil or substrate is periodically saturated with or covered with water.",
    "name": "Emergent Herbaceous Wetlands"
  }
}


#
#  map big zones to small zones
# useful for indexing the regional downloads
#

bigzones = {
  "1": [ 1, 2, 7, 8, 9],
  "2": [ 12, 13, 3, 4, 5, 6],
  "3": [ 10, 18, 19, 20, 21],
  "4": [ 16, 17, 22, 23, 28],
  "5": [ 14, 15, 24, 25],
  "6": [ 29, 30, 31, 39, 40],
  "7": [ 26, 27, 33, 34],
  "8": [ 41, 50, 51],
  "9": [ 38, 42, 43, 44],
  "10": [ 32, 35, 36],
  "11": [ 47, 49, 52, 53, 62],
  "12": [ 45, 48],
  "13": [ 60, 61, 63, 64, 65, 66],
  "14": [ 54, 55, 56, 57, 58, 59]
}

#
# maps zone to bigzone
#
#zones = dict(reduce(list.__add__, [[(zone, int(bigzone))
#                                    for zone in bigzones[bigzone]]
#                                   for bigzone in bigzones.keys()]))

