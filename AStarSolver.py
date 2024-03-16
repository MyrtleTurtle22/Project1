###### CURTIS DECKER #######


import json
from sklearn.metrics.pairwise import haversine_distances
from math import radians
from open_list import OpenList as OL
import sqlite3 as sl

    
def calc_haversine_distance(start_y, start_x, dest_y, dest_x):
    starting_latlon = [start_y, start_x]
    dest_latlon = [dest_y, dest_x]
    start_in_radians = [radians(_) for _ in starting_latlon]
    dest_in_radians = [radians(_) for _ in dest_latlon]
    h_distance = (haversine_distances([start_in_radians, dest_in_radians]) * 6371)[0][1]
    return h_distance

def make_path(came_from, current):
    total_path = [current]
    while current in came_from.keys():
        current = came_from[current]
        total_path.append(current)
    return total_path

def AStarSolver(start_node, dest_node, verbosity = 0):
    # Pseudocode for algorithm found here, although I modified it significantly
    # Section 3.2
    # https://www.mdpi.com/1999-4893/13/12/308

    # connect to DB to access node data
    conn = sl.connect('nodes.db')
    cursor = conn.cursor()
    
    # create open list and closed list, initialize g-score
    open_list = OL()
    closed_list = []
    came_from = {} # tracks the currently followed path
    g_score = {} # cost from start node to node n
    
    # get lat/lon of starting node
    query = cursor.execute("SELECT * FROM locations WHERE id = ?", (start_node,))
    sn_row = query.fetchone()
    sn_lat = sn_row[1]
    sn_lon = sn_row[2]
    
    # get lat/lon of destination node
    query = cursor.execute("SELECT * FROM locations WHERE id = ?", (dest_node,))
    dest_row = query.fetchone()
    dest_lat = dest_row[1]
    dest_lon = dest_row[2]
    
    # add starting node to open list
    open_list.add_node(start_node, calc_haversine_distance(sn_lat, sn_lon, dest_lat, dest_lon))
    g_score[start_node] = 0

    # get neighbors of current node
    while not open_list.isEmpty(): # if open list is empty and no solution is found, then fail

        if verbosity > 0:
            print("CLOSED LIST")
            print(closed_list)
            print("OPEN LIST")
            print(OL.__str__())
            print("CURRENT PATH")
            print(make_path(came_from, current))


        # remove min value from open list, Step 2
        current = open_list.remove_min() 
        closed_list.append(current)

        # if current is destination, then terminate, Step 3
        if current == dest_node:
            route = make_path(came_from, dest_node)
            route.reverse()
            conn.close()
            return route

        # get neighbor nodes of current node    
        children = cursor.execute("SELECT children FROM locations WHERE id = ?", (current,))
        children = children.fetchone()
        children = children[0]
        neighbors = json.loads(children)

        # iterate through nodes, calculating f-score of each
        for n in neighbors.keys():
            if n not in closed_list:

                # get lat/lon of neighbor to calculate haversine distance
                neighbor = cursor.execute("SELECT * FROM locations WHERE id = ?", (n,))
                neighbor = neighbor.fetchone()
                n_lat = neighbor[1]
                n_lon = neighbor[2]
                temp_h_score = calc_haversine_distance(dest_lat, dest_lon, n_lat, n_lon)

                # calculate cost function, Step 4
                temp_g_score = g_score[current] + neighbors.get(n)
                temp_f_score = temp_g_score + temp_h_score

                # if neighbor is not on open list, add it, Step 5
                if not open_list.is_present(int(n)):
                    open_list.add_node(int(n), temp_f_score)
                    came_from[int(n)] = current
                    g_score[int(n)] = temp_g_score

                # if neighbor is on open list but new f-score is lower, update it, Step 6
                elif temp_f_score < open_list.get_value(int(n)):
                    open_list.update_node(int(n), temp_f_score)
                    came_from[int(n)] = current
                    g_score[int(n)] = temp_g_score
    conn.close()
    # if open list is empty before destination node is found, then no route is possible
    return "FAIL"