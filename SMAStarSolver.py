import osmnx as ox
import json
import matplotlib.pyplot as plt
import matplotlib.patheffects as PathEffects
import networkx as nx
from sklearn.metrics.pairwise import haversine_distances
from math import radians
import heapq

columbia_data = json.loads("district-of-columbia-latest.osm.pbf")