# Author: Philippe Keita
import json
# from queue import PriorityQueue
# from sklearn.metrics.pairwise import haversine_distances
from Node import Node
from Queue import Queue
from AStarSolver import calc_haversine_distance

# Our bound for SMA*
MAX_NODE = 5
INFINITY = 1000000000

# This loads the data into 
columbia_data = None
with open("nodes.json", "r") as file:
    columbia_data = json.load(file)

def node_factory(node_id: str) -> Node:
    '''This method creates a Node object from an id provided
    The id reasearcht the global data from the json and created the node
    returns: the Node object created'''
    lat = columbia_data[node_id]['lat']
    lon = columbia_data[node_id]['lon']
    f = 0.0
    saved_f = 0.0
    parent = None
    children = [key for key in columbia_data[node_id]['neighbors'].keys()]
    return Node(node_id, lat, lon, f, saved_f, parent, children)

def update_f(node: Node, queue: Queue):
    print(f"---> Starting update. current node is {node.get_id()}")
    smallest = 0 # will serve as our min
    children_to_compare = [node_id for node_id in node.get_children() if queue.is_present(node_id)]
    if len(children_to_compare) != 0:
        smallest = queue.get_node(children_to_compare[0]).get_f()
        for i in range(1, len(children_to_compare)):
            if queue.get_node(children_to_compare[i]).get_f() < smallest:
                smallest = queue.get_node(children_to_compare[i]).get_f()
        if node.get_saved_f() != 0.0:
            node.set_f(min(smallest, node.get_saved_f()))  
        else:
            node.set_f(smallest)
        print(node.to_string())
    else:
        print("UNUSUAL CASE")
             
    if node.parent is None:
        print("Done updating")
        return
    update_f(node.parent, queue)

def all_successors_enqueued(node: Node, queue: Queue) -> bool:
    for child in node.children:
        if child not in queue.get_node_ids():
            return False
    return True
    
def get_solution(queue: Queue, goal_node: str, root_node: str, solution: Queue):
    print(f"goal: {goal_node} root: {root_node}")
    if goal_node == root_node:
        return solution.get_node_ids()
    else:
        goal_node = queue.get_node(goal_node)
        solution.add_node(goal_node.get_parent())
        get_solution(queue, goal_node.get_parent().get_id(), root_node, solution)

def MSA(root_node_id: str, goal_node_id: str) -> bool:
    """Runs solution and returns true if solution was found and
    false otherwise for now."""

    # Creating root node for algorithm
    root_node = node_factory(root_node_id) 
    print("ROOT NODE: ")
    print(root_node.to_string())
    # Creating  goal node
    goal_node = node_factory(goal_node_id)
    print("GOAL NODE: ")
    print(goal_node.to_string())
    # Setting f value for root node f = 0 + distance to goal
    print("Updating root node value with heuristic")
    root_node.set_f(calc_haversine_distance(root_node.get_lat(), root_node.get_lon(), goal_node.get_lat(), goal_node.get_lon()))
    print("ROOT NODE: ")
    print(root_node.to_string())

    # Creating a queue
    queue = Queue()
    print("QUEUE CREATED")
    print(queue.to_string())
    queue.add_node(root_node)
    print("ROOT NODE ADDED")
    print(queue.to_string())

    print("STARTING SEARCH ...")
    while True:
        # Return failure if the queue is empty AKA there is no solution
        print("Checking if queue is empty ...")
        print(f"---> queue is empty: {queue.isEmpty()}")
        if queue.isEmpty():
            print("NO SOLUTION. returning ...")
            return []

        # Getting Node to expand 
        print("Finding node to expand")
        current = queue.expand_deepest()
        # This should never happen but you never know
        if current is  None:
            print("Expanding returned None. returning ...")
            return []
        print(f"---> deepest least-f-cost node: {current.get_id()}")
        print(current.to_string())
        
        # If the node is the goal we have a solution
        print("Checking if accessed node is goal node")
        print(f"---> current node id == goal node id: {current.get_id() == goal_node_id}")
        if current == goal_node:
            print("SOLUTION IS FOUND. returning ...")
            print(queue.to_string())
            solution = Queue()
            solution.add_node(goal_node)
            return get_solution(queue, goal_node_id, root_node_id, solution)
        
        # Get successor 
        print("Getting successor to current")
        successor_id = current.get_successor()
        if successor_id is None: 
            print("returning ...")
            return []
        print(f"---> successor is {successor_id}")
        print("Creating successor node object")
        successor = node_factory(successor_id)
        successor.set_parent(current)
        print("---> successor node: ")
        print(successor.to_string())
        # print("---> current node is now: (Make sure successors are updated but not children)")
        # print(current.to_string())

        # If successor exploring not promising we assign infinity
        print("checking if node is promising")
        if successor != goal_node and successor.get_depth() == MAX_NODE:
            print("---> successor is not promising assiging infinity")
            successor.set_f(INFINITY)
            print(successor.to_string())
        else:
            # Set f to the max between the two 
            print("---> successor is promising. Reassiging calculated f to successor")
            f = max(current.get_f(), successor.get_parent().get_f() + calc_haversine_distance(successor.get_lat(), successor.get_lon(), goal_node.get_lat(), goal_node.get_lon()))
            successor.set_f(f)
            print(f"---> calculated f: {f}")
            print("---> successor is now: ")
            print(successor.to_string())
        # If all successors explored
        print("Checking if the current node has more successors to search...")
        if current.all_visited():
            print("---> all successors visited. Updating f values...")
            update_f(current, queue)

        # If successor all in memory then remove current node from queue
        print("Checking if all successors nodes are enqueued")
        if all_successors_enqueued(current, queue):
            print("---> all successors enqueued")
            print("Removing current node from queue")
            queue.remove_node(current)
            print("---> queue is now: ")
            print(queue.to_string())
        # Checking if memory is full
        print("Checking if memory is full")
        print(f"queue size: {queue.size()}, max nodes: {MAX_NODE}")
        if queue.size() == MAX_NODE:
            print("---> Memory is full. Forgetting node")
            queue.forget_node()
            print(queue.to_string())
            # queue.get_node(shallowest.parent.get_is()).remove_successor(shallowest.get_id())
            # if needed then queue.insert(parent); Dont know what this means

        print("Adding successor")
        queue.add_node(successor)
        print("---> Our queue")            
        print(queue.to_string())
    


def main():
    solution = MSA("310748060", "314662007")
    print(solution)

if __name__ == "__main__":
    main()