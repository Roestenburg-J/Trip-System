import random
import json
import os.path
import numpy as np

variable_item_size = True #Set to false to make each individual trip to carry the same number of individual items

if variable_item_size :
    min_num_items_per_trip = 2 
    max_num_items_per_trip = 10
else:
    num_items_per_trip = 10 #set if variable_item_size is set to False


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


def add_random_route_to_end(route , merch): 
    permutation = random.sample(range(0, len(neighbour_list[route[len(route)-1]])) , len(neighbour_list[route[len(route)-1]]))
    for i in permutation:                                                         # does not add city already in the route
        city = neighbour_list[route[0]][i]
        if not city in route:
            route.insert(0,city)
            break

    permutation = random.sample(range(0, len(items)), random.randint(min_num_items_per_trip if variable_item_size else num_items_per_trip ,max_num_items_per_trip if variable_item_size else num_items_per_trip))
    merch.append({items[k]:random.randint(1,20) for k in permutation})
    



def add_random_route_to_front(route , merch):
    permutation = random.sample(range(0, len(neighbour_list[route[0]])) , len(neighbour_list[route[0]]))
    for i in permutation:                                                         # does not add city already in the route
        city = neighbour_list[route[0]][i]
        if not city in route:
            route.insert(0,city)
            break

    permutation = random.sample(range(0, len(items)), random.randint(min_num_items_per_trip if variable_item_size else num_items_per_trip ,max_num_items_per_trip if variable_item_size else num_items_per_trip))
    merch.insert(0,{items[k]:random.randint(1,20) for k in permutation})



def edit_random_items(merch,edit_num):
    names = []
    values = []
    for key, value in merch.items():
        names.append(key)
        values.append(value)

    if edit_num > len(merch):
        edit_num = len(merch)

    for i in random.sample(range(0, len(merch)), edit_num):
        while True:                                                             # ensures that we do not have negative or zero quantity
            gen = random.randint(-merch_edit_amount, merch_edit_amount)
            if gen + values[i] > 0:
                merch[names[i]] = values[i] + gen
                break

    
def del_random_items(merch, del_num):
    names = list(merch.keys())

    if del_num >= len(merch):
        return
    for i in random.sample(range(0, len(merch)-1), del_num):
        del merch[names[i]]



def add_random_items(merch, add_num):    # does not add item already in the list
    names = list(merch.keys())
    i=0 
    count= 0
    permutation = random.sample(range(0, len(items)), len(items))

    # Add item not already in the list 
    while i < add_num: 
        if not items[permutation[count]] in names:
            merch[items[permutation[count]]]=random.randint(1,20)
            i+=1 

        count+= 1
        if count == len(items):
            return



def add_random_trip(routes , merchs):                                       # Add random trip in the middle of the route
    
    permutation = random.sample(range(0, len(routes)-1), len(routes)-1)     # Random permutation to try add a trip
    found = False
    for k in permutation:
        if k == 0:
            add_random_route_to_front(routes, merchs)
            return
        elif k == len(routes)-1:
            add_random_route_to_end(routes, merchs)
            return

        prev_city = routes[k-1]
        next_city = routes[k]
        common_neighbors = find_common_neigh(prev_city,next_city, neighbour_list)

        if len(common_neighbors) != 0:
            picked = random.choice(common_neighbors)
            found = True
            break

    if not found:
        print("No common neighbours")
        return
    
    routes.insert(k , picked)
    merch_list = list(merchs)
    for i in range(-1,1):
        permutation = random.sample(range(0, len(items)), random.randint(min_num_items_per_trip if variable_item_size else num_items_per_trip ,max_num_items_per_trip if variable_item_size else num_items_per_trip))
        food_list = {items[l]:random.randint(1,20) for l in permutation }
        merch_list.insert(i+k , food_list)

    merchs.clear()
    for lists in merch_list:
        merchs.append(lists)


def remove_front(routes , merchs):
    del routes[0]
    del merchs[0]

def remove_end(routes , merchs):
    del routes[len(routes)-1]
    del merchs[len(merchs)-1]

def remove_trip_at(ind , routes , merchs):
    prev_city = routes[ind-1]
    next_city = routes[ind]
    common_neighbors = find_common_neigh(prev_city,next_city, neighbour_list)

    if len(common_neighbors) == 0:      # No common neighbours
        return False
    
    picked = random.choice(common_neighbors)
    
    routes.insert(ind , picked)
    merch_list = list(merchs)
    for i in range(-1,1):
        permutation = random.sample(range(0, len(items)), random.randint(min_num_items_per_trip if variable_item_size else num_items_per_trip ,max_num_items_per_trip if variable_item_size else num_items_per_trip))
        food_list = {items[l]:random.randint(1,20) for l in permutation }
        merch_list.insert(i+ind , food_list)

    merchs.clear()
    for lists in merch_list:
        merchs.append(lists)
    
    return True

def remove_random_trip(routes , merchs): 
    if len(routes) < 3:
        return 
    
    permutation = random.sample(range(0, len(routes)-1), len(routes)-1)     # Random permutation to try add a trip

    for k in permutation:
        if k == 0:
            remove_front(routes , merchs)
        elif k == len(routes)-1:
            remove_end(routes , merchs)
        else:
            if not remove_trip_at(k,routes , merchs ):
                continue
        return

def convert_to_JSON(JSON_list, id, routes, merchs):
    city_to_city = []
    for j in range(len(routes) - 1):
        merchandise = []
        for item, quantity in merchs[j].items():
            merchandise.append({"item": item, "quantity": quantity})
        city_to_city.append({"from": routes[j], "to": routes[j + 1], "merchandise": merchandise})

    JSON_list.append({"id": id, "route": city_to_city})




def create_neighbour_list(neighbour_list, A):
    for i in range(len(A)):
        temp = []
        for j in range(len(A)):
            if A[i][j] == 1:
                temp.append(j)
        
        neighbour_list.append(temp)


def find_common_neigh(a,b,neighbour_list):
    lists = []
    if len(neighbour_list[a]) > len(neighbour_list[b]):
        smaller_list = neighbour_list[b]
        bigger_list = neighbour_list[a]
    else:
        smaller_list = neighbour_list[a]
        bigger_list = neighbour_list[b]

    for i in smaller_list:
        ind = binary_search(bigger_list , i)
        if ind != -1:
            lists.append(i)
    
    return lists
        

def binary_search(arr, x):
    low = 0
    high = len(arr) - 1
    mid = 0
 
    while low <= high:
        mid = (high + low) // 2
 
        if arr[mid] < x:
            low = mid + 1
        elif arr[mid] > x:
            high = mid - 1
        else:
            return mid
    # If we reach here, then the element was not present
    return -1
    

def conv_city_names(Routes):
    for i in range(len(Routes)):
        for j in range(len(Routes[i])):
            Routes[i][j] = cities.index(Routes[i][j])
        


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
A = np.loadtxt(os.path.dirname(__file__) + '/../data/matrix.txt', usecols=range(len(cities)))

neighbour_list = []
create_neighbour_list(neighbour_list, A)
conv_city_names(Routes)

# G = nx.from_numpy_array(np.array(A)) 
# mapping = {i:cities[i] for i in range(len(cities))}
# G = nx.relabel_nodes(G, mapping)

B_to_GB = 1024*1024*1024  # size of 1GB
# target_size = B_to_GB * 50 # Target size in GB , 
target_size = 1024 # Target size in GB , 

output_file = os.path.dirname(__file__) + '/../data/output.json'  # Path to the output file

# if not os.path.exists(output_file):
#     f = open(output_file, "w")
#     f.write("[]")
#     f.close()
# print(find_common_neigh(5 , 6 , neighbour_list))

# ...

with open(output_file, mode="w+") as file:
    file.write("[")

    new_id = 0
    mean = 3
    sd = 3

    # Generate distribution of numbers
    rand_list = np.random.normal(loc=mean, scale=sd, size=100)
    rand_dist_list = []
    # Convert numbers to positive int
    for i in range(len(rand_list)):
        rand_dist_list.append(int(abs(round(rand_list[i]))))

    while os.path.getsize(output_file) < target_size:
        picked = random.randint(0, len(Routes) - 1)  # Pick random route
        routes = Routes[picked].copy()
        merchs = Merchs[picked].copy()

        num_remove_trip = rand_dist_list[random.randint(0, len(rand_dist_list) - 1)]
        num_add_trip = rand_dist_list[random.randint(0, len(rand_dist_list) - 1)]

        for i in range(num_add_trip):
            add_random_trip(routes, merchs)

        for i in range(num_remove_trip):
            remove_random_trip(routes, merchs)

        for j in range(len(merchs)):
            num_remove_merch = rand_dist_list[random.randint(0, len(rand_dist_list) - 1)]
            num_add_merch = rand_dist_list[random.randint(0, len(rand_dist_list) - 1)]
            num_edit_merch = rand_dist_list[random.randint(0, len(rand_dist_list) - 1)]

            del_random_items(merchs[j], num_remove_merch)
            add_random_items(merchs[j], num_add_merch)
            edit_random_items(merchs[j], num_edit_merch)

        city_to_city = []
        for j in range(len(routes) - 1):
            merchandise = []
            for item, quantity in merchs[j].items():
                merchandise.append({"item": item, "quantity": quantity})
            city_to_city.append({"from": cities[routes[j]], "to": cities[routes[j + 1]], "merchandise": merchandise})

        json_output = json.dumps({"id": new_id, "route": city_to_city}, indent=3, sort_keys=False)
        file.write(json_output)
        if os.path.getsize(output_file) < target_size:
            file.write(",\n")

        new_id += 1

    file.write("]")

print("Output file reached the target size!")
