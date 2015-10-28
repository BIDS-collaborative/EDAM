# read in data for birds based on 110 sq km grain
bird_data = read.csv("~/Downloads/Supplementary Data 2/Meyer_etal_data_aves_110km.csv", sep=";")
reduced_bird_data = bird_data[, c("Latitude", "Longitude", "LandArea", "SpeciesRichness_Records", 
                                  "SpeciesRichness_Expert", "InventoryCompleteness", "NSpecies_Missed")]

# return true if x is between min and max
between = function(x, min, max) {
  return(x > min & x < max)
}

# clean data - convert from factor into numeric
latitude_levels = as.numeric(gsub(",", ".", levels(reduced_bird_data[, "Latitude"])))
longitude_levels = as.numeric(gsub(",", ".", levels(reduced_bird_data[, "Longitude"])))
completeness_levels = as.numeric(gsub(",", ".", levels(reduced_bird_data[, "InventoryCompleteness"])))
area_levels = as.numeric(gsub(",", ".", levels(reduced_bird_data[, "LandArea"])))

numeric_latitude = latitude_levels[as.numeric(reduced_bird_data[, "Latitude"])]
numeric_longitude = longitude_levels[as.numeric(reduced_bird_data[, "Longitude"])]
numeric_completeness = completeness_levels[as.numeric(reduced_bird_data[, "InventoryCompleteness"])]
numeric_area = area_levels[as.numeric(reduced_bird_data[, "LandArea"])]

# create new data frame of numeric data
numeric_bird_data = data.frame(numeric_latitude, numeric_longitude, numeric_area, 
                               reduced_bird_data[, "SpeciesRichness_Records"], 
                               reduced_bird_data[, "SpeciesRichness_Expert"], 
                               reduced_bird_data[, "NSpecies_Missed"], numeric_completeness)
names(numeric_bird_data) = c("Latitude", "Longitude", "LandArea", "SpeciesRecords", "SpeciesExpert",
                             "SpeciesMissed", "Completeness")

# 110 km is equivalent to about 1 degree latitude/longitude
# find data islands
galapagos_data = numeric_bird_data[between(numeric_bird_data[, "Latitude"], -1, 0) & between(numeric_bird_data[, "Longitude"], -91, -90), ]
kauai_data = numeric_bird_data[between(numeric_bird_data[, "Latitude"], 21, 22) & between(numeric_bird_data[, "Longitude"], -160, -159), ]
moorea_data = numeric_bird_data[between(numeric_bird_data[, "Latitude"], -18, -17) & between(numeric_bird_data[, "Longitude"], -150, -149), ]
friday_harbor_data = numeric_bird_data[between(numeric_bird_data[, "Latitude"], 48, 49) & between(numeric_bird_data[, "Longitude"], -124, -123), ]
