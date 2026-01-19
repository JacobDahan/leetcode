"""
# Definition for a Node.
class Node:
    def __init__(self, val = 0, neighbors = None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []
"""

from collections import deque
from typing import Optional

class Solution:
    """
    Given a reference of a node in a connected undirected graph.

    Return a deep copy (clone) of the graph.
    """

    def cloneGraph(self, node: Optional['Node']) -> Optional['Node']:
        """
        - We are provided a node from which we are asked to clone the graph that it is a part of
        - Ultimately, this means we must explore the entire graph (O(V + E) runtime complexity, dominated by V or E depending on the shape of the graph)
        - This also means we can use DFS or BFS -- we will traverse the entire graph, so it does not matter!
        - ... However, it may be more "natural" to use BFS, since we will explore one "layer" of neighbors at a time (O(V) space complexity in worst case)

        Algorithm:
        - Initialize a queue with the provided root node as our starting position, along with its neighbors
        - For each neighbor, clone the node and add it (and ITS neighbors) to the queue
        - Because this is a undirected graph, track what nodes have been visited to avoid cycles
        """
        if not node:
            return None
        
        # initialize the queue for BFS: queue the original node so that we can traverse its neighbors
        queue = deque([node])

        # every time we queue an element, mark it as seen AND store its clone so we can O(1) find it later
        visited = { node.val: Node(node.val) }

        # continue until the graph is fully traversed...
        while queue:
            n = queue.popleft()

            for neighbor in n.neighbors:
                # if we haven't seen this neighbor before...
                if neighbor.val not in visited:
                    # ... first, clone it (loosely) ...
                    neighbor_clone = Node(neighbor.val)
                    # ... next, mark it as visited so that we don't clone it elsewhere ...
                    visited[neighbor.val] = neighbor_clone
                    # ... finally, add the neighbor to the queue so that we can process ITS neighbors ...
                    queue.append(neighbor)
                
                # add the neighbor to the list of neighbors for this node
                node_copy = visited[n.val]
                node_copy.neighbors.append(visited[neighbor.val])
        
        return visited[node.val] # this is the root node from the input