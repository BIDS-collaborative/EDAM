import csv
from species.models import Plant


def convertNAtofloat(value):
	try: 
		value = float(value)
	except:
		value = float("nan")
	return value

with open("pier_data_wide.csv") as f:
    reader = csv.reader(f)
    for row in reader:
    	plant = Plant(
			name = row[0],
			domesticated = convertNAtofloat(row[1]),
			naturalized_where_grown = convertNAtofloat(row[2]),
			weedy_races = convertNAtofloat(row[3]),
			tropical_suitable_climate = convertNAtofloat(row[4]),
			suitable_climate_quality = convertNAtofloat(row[5]),
			broad_suitable_climate = convertNAtofloat(row[6]),
			tropical_naturalized = convertNAtofloat(row[7]),
			repeated_history_introduction = convertNAtofloat(row[8]),
			naturalized_beyond_natural = convertNAtofloat(row[9]),
			garden_weed = convertNAtofloat(row[10]),
			agricultural_weed = convertNAtofloat(row[11]),
			environmental_weed = convertNAtofloat(row[12]),
			congeneric_weed = convertNAtofloat(row[13]),
			spines_production = convertNAtofloat(row[14]),
			allelopathic = convertNAtofloat(row[15]),
			parasitic = convertNAtofloat(row[16]),
			unplatable_grazing_animals = convertNAtofloat(row[17]),
			toxicity_animals = convertNAtofloat(row[18]),
			pests_or_pathogens_host = convertNAtofloat(row[19]),
			alleric_or_toxic_humans = convertNAtofloat(row[20]),
			fire_hazard = convertNAtofloat(row[21]),
			shade_tolerant = convertNAtofloat(row[22]),
			soil_conditions_tolerance = convertNAtofloat(row[23]),
			climbing_growth_habit = convertNAtofloat(row[24]),
			dense_thickets = convertNAtofloat(row[25]),
			aquatic = convertNAtofloat(row[26]),
			grass = convertNAtofloat(row[27]),
			nitrogen_fixing_woody = convertNAtofloat(row[28]),
			geophyte = convertNAtofloat(row[29]),
			reproductive_failure_native_habitat = convertNAtofloat(row[30]),
			viable_seed = convertNAtofloat(row[31]),
			hybridizes_naturally = convertNAtofloat(row[32]),
			apomictic = convertNAtofloat(row[33]),
			requires_specialist_pollinators = convertNAtofloat(row[34]),
			vegetation_fragmentation_reproduction = convertNAtofloat(row[35]),
			minimum_generative_time = convertNAtofloat(row[36]),
			likely_unintentional_dispersal = convertNAtofloat(row[37]),
			human_intentional_dispersal = convertNAtofloat(row[38]),
			likely_produce_containment_dispersal = convertNAtofloat(row[39]),
			adapted_to_wind_dispersal = convertNAtofloat(row[40]),
			water_dispersal = convertNAtofloat(row[41]),
			bird_dispersal = convertNAtofloat(row[42]),
			animal_dispersal = convertNAtofloat(row[43]),
			survive_passage_through_gut = convertNAtofloat(row[44]),
			prolific_seed_production = convertNAtofloat(row[45]),
			persistent_propagule_bank = convertNAtofloat(row[46]),
			well_controlled_herbicides = convertNAtofloat(row[47]),
			tolerates_fire = convertNAtofloat(row[48]),
			natural_enemies_present = convertNAtofloat(row[49])
        	)
    	plant.save()