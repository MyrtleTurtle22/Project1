from pyrosm import OSM
import osmnx as ox


osm = OSM("district-of-columbia-latest.osm.pbf")
nodes, edges = osm.get_network(nodes=True, network_type = "driving")
# edges.head()
G = osm.to_graph(nodes, edges, graph_type="networkx")

ox.plot_graph_route(G, [49716206, 49716208, 49716210, 49716212, 49716214, 49857286, 49857284, 49857282, 49857280, 49857279, 49857278, 49857276, 49857274, 49857272, 49857270, 49841592, 49857267, 49857265, 49857263, 49857261, 49857259, 49857257, 49857256, 49857254, 49857252, 49857249, 49716219, 49716220, 49716221, 49716222, 49716223], route_linewidth=4, route_alpha=0.5)