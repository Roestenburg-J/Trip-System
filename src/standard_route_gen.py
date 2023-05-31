import random
import json
import os.path

number_of_standard_trips = 10 # Total number of trips to be generated

variable_trip_size = True #Set to false to make all full trips to be equal length
variable_item_size = True #Set to false to make each individual trip to carry the same number of individual items



if variable_item_size :
    min_num_items_per_trip = 2 
    max_num_items_per_trip = 10
else:
    num_items_per_trip = 10 #set if variable_item_size is set to False



if variable_trip_size :
    min_num_cities_per_standard_trip = 2 
    max_num_cities_per_standard_trip = 10
else:
    num_cities_per_standard_trip = 10 #set if variable_trip_size is set to False



def Generate_Random_Standard_Trip(length):
    permutation = random.sample(range(0, len(cities)), length+1)

    # random.shuffle(cities)                
    trip=[cities[permutation[i]] for i in range(length+1)]
    return trip

def Generate_All_Standard_Trips(length):
    all_standard_routes = []
    for i in range(length):
        if variable_trip_size:
            num = random.randint(min_num_cities_per_standard_trip, max_num_cities_per_standard_trip)
            all_standard_routes.append(Generate_Random_Standard_Trip(num))
        else:
            all_standard_routes.append(Generate_Random_Standard_Trip(num_cities_per_standard_trip))
            

    return all_standard_routes

def Convert_Routes_TO_JSON(all_standard_routes):
    json_list = []
    for i in range(len(all_standard_routes)):
        city_to_city = []
        for j in range(len(all_standard_routes[i])-1):
            permutation = random.sample(range(0, len(items)), random.randint(min_num_items_per_trip if variable_item_size else num_items_per_trip ,max_num_items_per_trip if variable_item_size else num_items_per_trip))

            # random.shuffle(items)                  # needs better optimisation
            food_list = {items[k]:random.randint(1,20) for k in permutation }
            city_to_city.append({'from' : all_standard_routes[i][j], 'to' :all_standard_routes[i][j+1], 'merchandise' : food_list})
        
        json_list.append({'id': i , 'route': city_to_city})

    return(json.dumps(json_list, indent=3,sort_keys=False))



cities = []
items = []

with open(os.path.dirname(__file__) + '/../data/cities.txt') as file:
    cities = [line.strip() for line in file]

with open(os.path.dirname(__file__) +'/../data/foods.txt') as file:
    items = [line.strip() for line in file]

print(Convert_Routes_TO_JSON(Generate_All_Standard_Trips(number_of_standard_trips)))