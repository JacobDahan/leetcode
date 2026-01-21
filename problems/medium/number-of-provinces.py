class Solution:
    """
    There are n cities. Some of them are connected, while some are not. If city a is connected directly with city b, and city b is connected 
    directly with city c, then city a is connected indirectly with city c.

    A province is a group of directly or indirectly connected cities and no other cities outside of the group.

    You are given an n x n matrix isConnected where isConnected[i][j] = 1 if the ith city and the jth city are directly connected, and isConnected[i][j] = 0 otherwise.

    Return the total number of provinces.
    """

    def findCircleNum(self, isConnected: List[List[int]]) -> int:
        """
        Task:
        - We are given an n x n matrix where isConnected[i][j] = 1 if the ith city and the jth city are directly
        - We are asked to find the total number of provinces, where a province is an "island" of connected cities

        Observations:
        - We *could* solve this in O(V + E) by iterating over the matrix and counting the number of islands (use DFS, BFS to explore
          each island and count the unique islands)
        - ... But it would be more efficient (O(alpha n), where alpha is approx. constant) to use disjoint set / union find to solve this
        - In union find, we can "union" connected elements in the graph, then "find" the root node of each component
        - If we build up a disjoint set of all of the connected elements, we can simply return the **unique number of root nodes**
        """
        class UnionFind():
            def __init__(self, size: int):
                self.roots = [i for i in range(size)] # each province is initial the root of its own graph until we union them together
                self.ranks = [1] * size # the initial "ranking" of each disconnected graph is the size of the graph -- the element itself
            
            def find(self, n: int) -> int:
                """
                Returns the root node for any given node n.
                Uses path compression optimization to reduce *future* lookups to O(log n).
                """
                if self.roots[n] == n:
                    return n # this is the root of itself! return n
                
                # find the root of the parent of n, and, for future queries, store that in n itself
                # this would be maximally O(n) on the first try (ignoring union by rank), but is reduced to O(log n)
                self.roots[n] = self.find(self.roots[n]) 
                # finally, return whatever we just calculated
                return self.roots[n]

            def union(self, x: int, y: int) -> bool:
                """
                Union the nodes x and y.
                Uses union by rank to make the tree as balanced as possible (i.e., puts the smaller tree "under" the bigger tree).
                If the trees are of equal size, uses x.

                Runtime is dominated by the find operation.
                By ensuring trees are well-balanced, this reduces find to O(log n) (the maximum height of the tree) (ignoring path compression).

                Returns True if the elements were not previously unioned, else False.
                """
                x_root = self.find(x)
                y_root = self.find(y)

                if x_root != y_root: # if the two are equal, there is no union to do! already in the same set
                    if self.ranks[x_root] > self.ranks[y_root]:
                        # X's root is "bigger", so throw Y under that root to balance the tree
                        self.roots[y_root] = x_root
                    elif self.ranks[y_root] > self.ranks[x_root]:
                        # Y's root is bigger, so throw X under that root
                        self.roots[x_root] = y_root
                    else:
                        # trees are same size, merge Y into X and grow X by one
                        self.roots[y_root] = x_root
                        self.ranks[x_root] += 1
                    
                    return True
                
                return False
        
        uf = UnionFind(len(isConnected))
        num_provinces = len(isConnected)

        for r in range(len(isConnected)):
            for c in range(r + 1, len(isConnected)): # any c <= r has already been checked by previous r (i.e., r = 1, c = 2 gives the same result as r = 2, c = 1)
                if isConnected[r][c] != 1: # not connected, do not union
                    continue

                if uf.union(r, c): # if we connected A and B, we've lost a province!
                    num_provinces -= 1
        
        return num_provinces