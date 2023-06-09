import random
import json
import os.path
import networkx as nx
import numpy as np

number_of_standard_trips = 10 # Total number of trips to be generated

variable_trip_size = False #Set to false to make all full trips to be equal length
variable_item_size = True #Set to false to make each individual trip to carry the same number of individual items

ave_degree = 10

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



def Generate_Random_Standard_Trip(length ):
    trip = []
    trip.append( cities[random.randint(0,len(cities)-1)])
    while len(trip) <= length:
        neighbours = list(nx.neighbors(G, trip[len(trip)-1]))
        random.shuffle(neighbours)
        found = False
        for neigh in neighbours:
            if not neigh in trip:
                trip.append(neigh)
                found = True
                break

        if not found:               # If length size not satisfied, then remove last city and try again
            trip.pop()

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

# G = nx.erdos_renyi_graph(len(cities), ave_degree/len(cities))
# mapping = {i:cities[i] for i in range(len(cities))}
# G = nx.relabel_nodes(G, mapping)
# A = nx.adjacency_matrix(G)
# A = A.todense()

# mat = np.matrix(A)
# with open('outfile.txt','wb') as f:
#     for line in mat:
#         np.savetxt(f, line, fmt='%.2f')

A = np.loadtxt(os.path.dirname(__file__) + '/../data/matrix.txt', usecols=range(len(cities)))
# print(A)
G = nx.from_numpy_array(np.array(A)) 
mapping = {i:cities[i] for i in range(len(cities))}
G = nx.relabel_nodes(G, mapping)

json_data = Convert_Routes_TO_JSON(Generate_All_Standard_Trips(number_of_standard_trips))

# Write JSON data to file
output_file = 'data/data.json'
with open(output_file, 'w') as file:
    file.write(json_data)

print(f"JSON data saved to {output_file}")
