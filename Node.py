# Author: Philippe Keita
# Data structure to hold the infomration from a node imported from 
# the json files. 

from typing import List

class Node: 
    def __init__(self, id: str, lat: float, lon: float, f: float = 0.0 , saved_f: float = 0.0, parent: 'Node' = None, children: List[str] = []):
        self.id = id
        self.lat = lat
        self.lon = lon
        self.f = f
        self.saved_f = saved_f
        self.parent = parent
        self.children = children
        self.all_successors_visited = False
        self.successor = children[0] if len(children) != 0 else None
        self.depth = parent.get_depth() + 1 if parent is not None else 1

    # Getters
    def get_id(self) -> int:
        return self.id
    
    def get_parent(self) -> 'Node':
        return self.parent
    
    def get_f(self) -> float:
        return self.f
    
    def get_saved_f(self) -> float:
        return self.saved_f
    
    def get_lat(self) -> float:
        return self.lat
    
    def get_lon(self) -> float:
        return self.lon
    
    def get_depth(self) -> int:
        return self.depth
    
    def get_successor(self) -> str:
        """Returns the next successor of the node from the children"""
        successor = self.successor
        if successor not in self.children:
            return None
        next = (self.children.index(successor) + 1) % len(self.children)
        self.successor = self.children[next]
        # If all the children we set all visited to true. Useful somewhere else
        if next == 0:
            self.all_successors_visited = True
        if next == 1 and self.all_successors_visited == True:
            self.all_successors_visited = False
        return successor
    
    def get_children(self) -> List[str]:
        return self.children

    # Setters
    def set_parent(self, parent: 'Node'):
        self.parent = parent
        self.depth = parent.get_depth() + 1
        self.children.remove(parent.get_id())
 
    def set_f(self, f):
        self.f = f

    def set_saved_f(self, f):
        self.saved_f = f
    
    # Other 
    def all_visited(self):
        return self.all_successors_visited
    
    # def remove_successor(self, successor_id):
    #     self.successors.remove(successor_id)
    
    # def has_successors(self):
    #     return len(self.successors) != 0
    
    def to_string(self):
        return f"""
        -------------------------------------------------------Node
        Node: {self}
        id: {self.id}
        parent: {self.parent.get_id() if self.parent is not None else "None"}
        coord: {self.lat}, {self.lon}
        children: {self.children}
        succcessors: {self.successor}
        f value: {self.f}
        saved f value: {self.saved_f}
        depth: {self.depth}
        -------------------------------------------------------
        """
    
    # The following allows for Node comparison

    # Equality comparison
    def __eq__(self, other):
        return self.get_id() == other.get_id()
    
    # Inequality comparison
    def __ne__(self, other):
        return not self.__eq__(other)
    
    # Less-than comparison
    def __lt__(self, other):
        return self.get_f() < other.get_f() if self.get_f() != other.get_f() else self.get_depth() > other.get_depth()
    
    # # Less-than or equal-to comparison
    # def __le__(self, other):
    #     return self.get_f() <= other.get_f() if self.get_f() != other.get_f() else self.get_depth() >= other.get_depth()
    
    # # Greater-than comparison
    # def __gt__(self, other):
    #     return self.get_f() > other.get_f() if self.get_f() != other.get_f() else self.get_depth() < other.get_depth()
    
    # # Greater-than or equal-to comparison
    # def __ge__(self, other):
    #     return self.get_f() >= other.get_f() if self.get_f() != other.get_f() else self.get_depth() <= other.get_depth()