import osmnx as ox
import json
import matplotlib.pyplot as plt
import matplotlib.patheffects as PathEffects
import networkx as nx
from sklearn.metrics.pairwise import haversine_distances
from math import radians
import heapq
import osmium as os

class OpenList:
    def __init__(self):
        self.open_list = {}
        self.heap = []

    def add_node(self, node_id, value):
        self.open_list[node_id] = value
        heapq.heappush(self.heap, (value, node_id))

    def update_node(self, node_id, new_value):
        self.open_list[node_id] = new_value
        self.heap = [(val, nid) for val, nid in self.heap if nid != node_id]
        heapq.heapify(self.heap)
        heapq.heappush(self.heap, (new_value, node_id))

    def remove_min(self):
        if self.heap:
            return heapq.heappop(self.heap)[1]
        else:
            return None
        
    def is_present(self, node_id):
        return node_id in self.open_list

    def get_value(self, node_id):
        return self.open_list.get(node_id, None)
    
    def isEmpty(self):
        return len(self.heap) == 0
    
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

nodes = json.loads("nodes.json")
# G = ox.graph_from_place('Bronx', network_type='drive')
# create open list and closed list, initialize g-score
open_list = OpenList()
closed_list = []
came_from = {}
g_score = {} # cost from start node to node n
# get starting node from coordinates and add to open list
nn = 2599168199
dest_node = 310748125
nn_lon = 0
nn_lat = 0
dest_lon = 0
dest_lat = 0
for i in nodes:
    if i["node_id"] == nn:
        nn_lon = i["lon"]
        nn_lat = i["lat"]
    else:
        Exception
for i in nodes:
    if i["node_id"] == dest_node:
        dest_lon = i["lon"]
        dest_lat = i["lat"]
    else:
        Exception

open_list.add_node(nn, calc_haversine_distance(nn_lat, nn_lon, dest_lat, dest_lon))
g_score[nn] = 0
# get destination node


# get neighbors of current node
while not open_list.isEmpty(): # if open list is empty and no solution is found, then fail
    # sort open list by value
    # current is the lowest value in open_list
    current = open_list.remove_min()
    closed_list.append(current)
    if current == dest_node:
        route = make_path(came_from, dest_node)
        route.reverse()
        print(route)
        # ox.plot_graph_route(G, route, route_color='r', route_linewidth=4, route_alpha=0.5)
    neighbors = []
    for i in nodes:
        if i["node_id"] == current:
            neighbors.append(i[neighbors])
    for n in neighbors:
        if n not in closed_list:
            # get lat/lon of current and each neighbor to calculate haversine distance
            d_lat = G.nodes[dest_node]['y']
            d_lon = G.nodes[dest_node]['x']
            n_lat = G.nodes[n]['y']
            n_lon = G.nodes[n]['x']
            temp_h_score = calc_haversine_distance(d_lat, d_lon, n_lat, n_lon)
            # calculate cost function
            temp_g_score = g_score[current] + G.edges[(current, n, 0)]["length"]/1000
            temp_f_score = temp_g_score + temp_h_score
            if not open_list.is_present(n):
                open_list.add_node(n, temp_f_score)
                came_from[n] = current
                g_score[n] = temp_g_score

            elif temp_f_score < open_list.get_value(n):
                open_list.update_node(n, temp_f_score)
                came_from[n] = current
                g_score[n] = temp_g_score