# Author: Philippe Keita (Code from Curtis that I edited)
from Node import Node
from typing import List
import heapq

class Queue:
    def __init__(self):
        self.nodes: List[Node] = []
        self.max_depth: int = 0

    def add_node(self, node: Node):
        self.nodes.append(node)
        self.max_depth = max(self.max_depth, node.get_depth())

    # def update_node(self, node: Node, new_value: float):
    #     self.open_list[node.get_id()] = new_value
    #     self.heap = [(val, nid) for val, nid in self.heap if nid.get_id() != node.get_id()]
    #     heapq._heapify_max(self.heap)
    #     heapq.heappush(self.heap, (new_value, node))
        
    def expand_deepest(self) -> Node:
        node_to_expand: Node = None
        # Finding lowest f value node
        lowest_f_nodes = [(node.get_f(), node) for node in self.nodes]
        heapq.heapify(lowest_f_nodes)
        # Should never happen i believe
        print(lowest_f_nodes)
        if len(lowest_f_nodes) != 0:
            # Extracting the min 
            node_to_expand = heapq.heappop(lowest_f_nodes)[1]
            # Checking if node is valid for expansion
            # while not node_to_expand.all_visited():     
        return node_to_expand
        

    # Change this so it removes the shallowest bla bla bla
    def forget_node(self):
        print(self.nodes) 
        nodes_list = [(node.get_f(), node) for node in self.nodes]
        heapq._heapify_max(nodes_list)
        print(nodes_list[0][0])
        print(nodes_list)
        nodes_list = [node for node in nodes_list if node[0] == nodes_list[0][0]][::-1]
        print(nodes_list)
        node_to_remove = heapq.heappop(nodes_list)[1]
        print(node_to_remove)
        print("Removing node: ")
        print(node_to_remove.to_string())
        # self.remove_node(node_to_remove)
        node_to_remove.get_parent().set_saved_f(node_to_remove.get_f())
        node_to_remove.get_parent().get_children().remove(node_to_remove.get_id())
        self.remove_node(node_to_remove)
        # for node in self.nodes:
        #     if node_to_remove.get_id() in node.children:
        #         node.set_saved_f(node_to_remove.get_f())
        
    def remove_node(self, to_remove: Node):
        for node in self.nodes:
            if node.get_id() == to_remove.get_id():
                self.nodes.remove(node)
        self.max_depth -= 1

    # TODO: Make this faster by having a dictionary for faster lookup
    def is_present(self, node_id: str):
        return node_id in [node.get_id() for node in self.nodes]


    # def get_value(self, node):
    #     return self.open_list.get(node.get_id(), None)
    
    def get_node(self, node_id):
        for node in self.nodes:
            if node.get_id() == node_id:
                return node
    
    def get_node_ids(self) -> List[str]:
        print([node.get_id() for node in self.nodes])
        return [node.get_id() for node in self.nodes]
    
    def isEmpty(self):
        return len(self.nodes) == 0

    def size(self):
        return len(self.nodes)

    def to_string(self):
        return f"""
        ---------------------------Queue-----------------------
        Nodes addresses: {self.nodes}
        Max_depth : {self.max_depth}
        Node ids: {[node.get_id() for node in self.nodes]}
        -------------------------------------------------------
        """