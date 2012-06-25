#! /usr/bin/env python
# spidertrot.py
#
# Python 2.7 implementation of the mathematics of Spidertrot.
# For details, refer to the associated documentation.

from __future__ import print_function

class Node(object):
    """
    Computer science model of a node in Spidertrot.

    For comparison purposes, a Node object is represented by its name.
    This is relevant for __hash__ and __eq__.
    """
    
    def __init__(self, name, value):
        self.name = name
        self.value = value
    
    def __repr__(self):
        return "Node(\"{}\", {})".format(self.name, self.value)

    def __str__(self):
        return self.name
    
    def __hash__(self):
        return hash(self.name)
    
    def __eq__(self, other):
        return isinstance(other, Node) and self.name == other.name

    def __ne__(self, other):
        return not (self == other)


def get_path_list_1(node_dict, curr_path_list=None):
    """
    If possible, constructs (recursively) and returns a list containing the
    nodes one must traverse, in order, to solve the puzzle. (Obviously, there
    can be more than one possibility; this function only finds one.)
    
    If the puzzle is impossible to solve, None is returned.
    
    node_dict is a dictionary where the keys are the nodes and the values
    are the number of times we can visit each node. If you have a list of
    nodes, node_dict is easily constructed with a dict comprehension:
    
    node_dict = {n: n.value for n in your_node_list}
    
    curr_path_list is a list of the nodes traversed so far. It's only used
    for the recursive algorithm, to memorize the paths already tried, but
    you can technically customize it if you want...just make sure to
    construct node_dict more carefully than above.

    Recurrence relation is approximately:
    
    T(n, m) = n * T(n, m-1) + O(n)
    
    where
    n = number of nodes (constant)
    m = sum of all nodes' values

    and T(n, 0) = O(1)
    
    which makes the function roughly O(n^m).
    """
    if curr_path_list is None:
        curr_path_list = []

    # search for an available path
    for n in node_dict:
        if (not curr_path_list or curr_path_list[-1] != n) and node_dict[n] > 0:
            d = node_dict.copy()
            d[n] -= 1
            path = get_path_list_1(d, curr_path_list + [n])
            if path is not None:
                return path

    # check if every node was exhausted
    for n in node_dict:
        if node_dict[n] != 0:
            return None
    
    return curr_path_list

def get_path_list_2(node_dict, target_value=0):
    """
    More efficient version of get_path_list, which exploits
    the structure of the path between the vertices to avoid
    brute-force searching.

    Recurrence relation is approximately:

    T(0) = O(1)
    T(1) = O(1)
    T(2) = O(k) where k = sum of node values - target value
    (which is O(1) in the number of nodes)

    and for n >= 3:
    T(n) = T(n-1) + O(kn)
    
    which makes the function roughly O((kn)^2).
    """

    # if there are no nodes, we're done
    if len(node_dict) == 0:
        return []

    # if there is a single node:
    # check to see if its value is 1
    # if it does, we're done
    # else the puzzle is impossible
    elif len(node_dict) == 1:
        n = node_dict.keys()[0]
        if node_dict[n] == 1:
            return [n]
        else:
            return None

    # if there are two nodes:
    # this is essentially the base case
    # check to see if reflecting between them will return
    # the target value, and if so, return true
    # else the puzzle is impossible
    elif len(node_dict) == 2:
        min_n = min(node_dict.keys(), key=lambda x: x.value)
        max_n = [n for n in node_dict if n is not min_n][0]
        sub_path_list = []
        
        curr_n = max_n
        # perform reflection technique
        while True:
            # use current node
            if node_dict[min_n] + node_dict[max_n] > target_value:
                # if it is possible to still subtract
                if node_dict[curr_n] >= 1:
                    # then do so
                    sub_path_list.append(curr_n)
                    node_dict[curr_n] -= 1
                # otherwise puzzle is impossible
                else:
                    return None
            else:
                break
                
            # switch to other node
            if curr_n == max_n:
                curr_n = min_n
            else:
                curr_n = max_n

        return sub_path_list

    # if there are 3+ nodes:
    # now time to recurse: find smallest key and exclude that
    # reflect between the remaining nodes, recursing downwards as
    # necessary (case for 2 nodes is the base)
    else:
        # find node that yields minimum value
        min_key = None
        for n in node_dict:
            if min_key not in node_dict:
                min_key = n
            else:
                if node_dict[n] < node_dict[min_key]:
                    min_key = n

        # recurse
        new_node_dict = {n: node_dict[n] for n in node_dict if n is not min_key}
        sub_path_list = get_path_list_2(new_node_dict, target_value+node_dict[min_key])
        if sub_path_list is None:
            return None

        # link solution with the min node
        node_dict.update(new_node_dict)
        for n in new_node_dict:
            # exhausted min node? done
            if node_dict[min_key] <= 0:
                break

            # otherwise, reflect it with any given node
            # until either is exhausted
            while node_dict[n] > 0 and node_dict[min_key] > 0:
                sub_path_list.append(min_key)
                sub_path_list.append(n)
                node_dict[n] -= 1
                node_dict[min_key] -= 1
        
        return sub_path_list
        
def output_path(node_list):
    """
    Outputs a series of lines that describe a solution for a puzzle as given
    by node_list (an iterable containing Node objects).
    """
    #path = get_path_list_1({n: n.value for n in node_list})
    path = get_path_list_2({n: n.value for n in node_list})
    
    if path is None:
        print("Impossible puzzle.")
        return
    
    path.insert(0, "start")
    path.append("end")
    for i in xrange(len(path[:-1])):
        print("Move from '{}' to '{}'.".format(str(path[i]), str(path[i+1])))

def main(default_nodes=None):
    if default_nodes is None:
        default_nodes = dict()
    
    nodes = {n: Node(n, default_nodes[n]) for n in default_nodes}
    while True:
        print()
        print("[0] Quit")
        print("[1] Add node")
        print("[2] Modify node")
        print("[3] Delete node")
        print("[4] Output solution to current puzzle")
        print()
        print("Current list of nodes:")
        for n in nodes:
            print("> {} ({})".format(n, nodes[n].value))
        print()
        choice = raw_input("Choice: ")
        print()

        if choice == "0":
            break

        elif choice == "1":
            name = raw_input("New node name? ")
            if name in nodes:
                print("That node name is already used.")
            else:
                value = int(raw_input("New node value? "))
                nodes[name] = Node(name, value)
            
        elif choice == "2":
            name = raw_input("Name of node to modify? ")
            if name not in nodes:
                print("That node does not currently exist.")
            else:
                value = int(raw_input("New node value? "))
                nodes[name].value = value

        elif choice == "3":
            name = raw_input("Name of node to delete? ")
            try:
                del nodes[name]
            except(KeyError):
                print("That node does not currently exist.")

        elif choice == "4":
            output_path(nodes.viewvalues())
        
        else:
            print("Invalid choice.")
            

if __name__ == "__main__":
    main({"alpha" : 1, "bravo" : 2, "charlie" : 3})
