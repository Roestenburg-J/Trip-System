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
add_p = 0.3  # percent of items to be added. If set to 1, then number of items will be doubled

merch_edit_amount = 10 # range of how much we can edit the quantity of each item



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


def add_random_route_to_end(route , merch): # does not add city already in the route
    permutation = random.sample(range(0, len(items)), random.randint(min_num_items_per_trip if variable_item_size else num_items_per_trip ,max_num_items_per_trip if variable_item_size else num_items_per_trip))
    while True:
        city = cities[random.randint(0,len(cities)-1)]
        if city in route:
            continue
        else:
            route.append(city)
            merch.append({items[k]:random.randint(1,20) for k in permutation})
            break


def add_random_route_to_front(route , merch): # does not add city already in the route
    permutation = random.sample(range(0, len(items)), random.randint(min_num_items_per_trip if variable_item_size else num_items_per_trip ,max_num_items_per_trip if variable_item_size else num_items_per_trip))

    while True:
        city = cities[random.randint(0,len(cities)-1)]
        if city in route:
            continue
        else:
            route.insert(0,city)
            merch.insert(0,{items[k]:random.randint(1,20) for k in permutation})
            break

# def add_random_route_to_mid(index): #??

def edit_random_items(merch):
    names = []
    values = []
    for key, value in merch.items():
        names.append(key)
        values.append(value)

    for i in random.sample(range(1, len(merch)), round(len(merch)*edit_p)):
        while True:                                                             # ensures that we do not have negative or zero quantity
            gen = random.randint(-merch_edit_amount, merch_edit_amount)
            if gen + values[i] > 0:
                merch[names[i]] = values[i] + gen
                break

    
def del_random_items(merch):
    names = []
    values = []
    for key, value in merch.items():
        names.append(key)
        values.append(value)

    for i in random.sample(range(0, len(merch)-1), round(len(merch)*del_p)):
        del merch[names[i]]



def add_random_items(merch):    # does not add item already in the list
    names = []
    values = []
    i=0 
    count= 0
    permutation = random.sample(range(0, len(items)), len(merch) + round(len(merch)*add_p))
    for key, value in merch.items():
        names.append(key)
        values.append(value)


    while i < round(len(merch)*add_p):
        if not items[permutation[count]] in names:
            merch[items[permutation[count]]]=random.randint(1,20)
            i+=1 

        count+= 1

def convert_to_JSON(JSON_list, id , routes , merchs):
    city_to_city = []
    for j in range(len(routes)-1):
        city_to_city.append({'from' : routes[j], 'to' :routes[j+1], 'merchandise' : merchs[j]})

    JSON_list.append({'id': id , 'route': city_to_city})


IDs = []
Routes = []
Merchs = []

with open(os.path.dirname(__file__) +'/../data/foods.txt') as file:
    items = [line.strip() for line in file]

with open(os.path.dirname(__file__) + '/../data/cities.txt') as file:
    cities = [line.strip() for line in file]

with open(os.path.dirname(__file__) + '/../data/data.json', 'r') as openfile:
    json_object = json.load(openfile)




Split_JSON_Obj(json_object)

new_id = 0
json_list = []

for i in range(len(Routes)):    # For each standard route, add a city to the start and end of the trips, additionally, edit and add items to each city-to-city trip
    
    routes = Routes[i].copy()
    merchs = Merchs[i].copy()

    # print(routes)
    # print(merchs)

    for merch in merchs:
        edit_random_items(merch)
        add_random_items(merch)

    # for route in routes:
    add_random_route_to_end(routes , merchs)
    add_random_route_to_front(routes , merchs)

    convert_to_JSON(json_list,new_id,routes, merchs)
    new_id += 1
    


print(json.dumps(json_list, indent=3,sort_keys=False))

