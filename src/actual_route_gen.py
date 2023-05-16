import random
import json
import os.path

variable_item_size = True #Set to false to make each individual trip to carry the same number of individual items

if variable_item_size :
    min_num_items_per_trip = 2 
    max_num_items_per_trip = 10
else:
    num_items_per_trip = 10 #set if variable_item_size is set to False

edit_p = 0.3  # percent of items to edit. If set to 1, then all item amounts will be edited
del_p = 0.3  # percent of items to be deleted. If set to 1, then all items will be deleted
add_p = 0.3  # percent of items to be added. If set to 1, then all items will be deleted







IDs = []
Routes = []
Merchs = []


def Split_JSON_Obj(json_object):
    for line in json_object:
        IDs.append(line['id'])
        route_obj = line['route']
        full_route = [route_obj[0]['from']]
        full_merch = []
        for r in route_obj:
            full_route.append(r['to'])
            full_merch.append(r['merchandise'])
        Routes.append(full_route)
        Merchs.append(full_merch)


def add_random_route_to_end(index): # does not add city already in the route
    route = Routes[index]
    merch = Merchs[index]
    while True:
        city = cities[random.randint(0,len(cities)-1)]
        if city in route:
            continue
        else:
            route.append(city)
            random.shuffle(items)                  # needs better optimisation
            merch.append({items[k]:random.randint(1,20) for k in range(random.randint(min_num_items_per_trip if variable_item_size else num_items_per_trip ,max_num_items_per_trip if variable_item_size else num_items_per_trip))})
            break


def add_random_route_to_front(index): # does not add city already in the route
    route = Routes[index]
    merch = Merchs[index]
    while True:
        city = cities[random.randint(0,len(cities)-1)]
        if city in route:
            continue
        else:
            route.insert(0,city)
            random.shuffle(items)                  # needs better optimisation
            merch.insert(0,{items[k]:random.randint(1,20) for k in range(random.randint(min_num_items_per_trip if variable_item_size else num_items_per_trip ,max_num_items_per_trip if variable_item_size else num_items_per_trip))})
            break

# def add_random_route_to_mid(index): #??

def edit_random_item(items):




with open(os.path.dirname(__file__) +'/../data/foods.txt') as file:
    items = [line.strip() for line in file]

with open(os.path.dirname(__file__) + '/../data/cities.txt') as file:
    cities = [line.strip() for line in file]

with open(os.path.dirname(__file__) + '/../data/data.json', 'r') as openfile:
    json_object = json.load(openfile)



Split_JSON_Obj(json_object)
print(Routes)
print(Merchs)
add_random_route_to_front(0)
print(Routes)
print(Merchs)
