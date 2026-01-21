from collections import defaultdict

class Solution:
    """
    You have a graph of n nodes. You are given an integer n and an array edges where edges[i] = [ai, bi] indicates 
    that there is an edge between ai and bi in the graph.

    Return the number of connected components in the graph.
    """

    def countComponents(self, n: int, edges: List[List[int]]) -> int:
        """
        Task:
        - We are given a list of EDGES, such that edges[i] = [ai, bi], representing an edge between ai and bi in the graph
        - We are asked to return the NUMBER of connected components in the graph

        Observations:
        - We can convert the provided EDGE LIST to an ADJACENCY LIST so that we can explore the graph
        - For each node in the adjacency list, we can explore all of its neighbors (BFS or DFS, does not matter)
            - We have to keep track of which nodes we've visited, because (1) this is undirected and possibly cyclic and (2) once we explore a component,
              there is no value in exploring it again
            - Each time that we see a node that we haven't visited before and explore its component, increase our counter by one (logically, if it was connected to
              another component, we would have already visited this via our prior exploration of that component)
        """

        # first, transform the edge list to an adjacency list so that we can more easily explore the graph
        adjacencies = defaultdict(list)
        for a, b in edges: # undirected graph, so no source or destination; visiting each edge is O(e) runtime; adjacency list is O(e) space
            adjacencies[a].append(b) # a --> b
            adjacencies[b].append(a) # b --> a
        
        visited = [False] * n # because each node is labeled [0, n - 1], we can use an array instead of a visited set; O(n) space complexity

        def explore(node: int):
            """
            Utility method to explore (using DFS) all neighbors of the provided node.
            Does not visit already-visited nodes.
            """
            visited[node] = True

            for neighbor in adjacencies[node]: # In sum over ALL the nodes in the graph, O(e) runtime complexity
                if not visited[neighbor]:
                    explore(neighbor)

        components = 0

        # next, iterate over and explore each of the nodes in the graph (O(n) runtime)
        for node in range(n): # O(n) runtime to iterate over each node
            # if we've seen the node before, do not re-visit
            if not visited[node]:
                explore(node)
                components += 1 # if we haven't seen this node, it must be part of a new (disconnected) component
        
        return components
    
### Complexity:
# Space - O(e + n); O(e) for the adjacency list; O(n) for the visited set
# Runtime - O(e + n); O(e) to visit all the adjacencies in the graph (and to create the adjacency list); O(n) to visit all the nodes in the graph

### Testing
# n = 5, edges = [[0,1],[1,2],[3,4]]
# adjacencies = {0: [1], 1: [0, 2], 2: [1], 3: [4], 4: [3]}, visited = [False, False, False, False, False]
# iteration 1: node = 0; components = 1; visited = [True, True, True, False, False]
# iteration 2: node = 1; components = 1; visited = [True, True, True, False, False]
# iteration 3: node = 2; components = 1; visited = [True, True, True, False, False]
# iteration 4: node = 3; components = 2; visited = [True, True, True, True, True]
# iteration 5: node = 4; components = 2; visited = [True, True, True, True, True] # return 2