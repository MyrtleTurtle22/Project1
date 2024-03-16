###### CURTIS DECKER ######

import heapq

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
    
    def __str__(self):
        return str(self.node_values)