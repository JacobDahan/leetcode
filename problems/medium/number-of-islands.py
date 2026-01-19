class Solution:
    """
    Given an m x n 2D binary grid grid which represents a map of '1's (land) and '0's (water), return the number of islands.

    An island is surrounded by water and is formed by connecting adjacent lands horizontally or vertically. 
    You may assume all four edges of the grid are all surrounded by water.
    """
    def numIslands(self, grid: List[List[str]]) -> int:
        """
        - We are tasked with counting the number of islands in an m x n grid
        - An island is a connected component (up/down/left/right-connected ONLY) surrounded by water or borders
        - If we explore the grid one cell at a time, we can skip any cell that is water
        - From any cell that is land, we can trivially explore the entire island with DFS or BFS (either works)
            - Since this is an undirected graph, we'll need to track a visited set to ensure we don't cycle
            - Because we'll be tracking what cells we've visited, we can skip re-exploring islands that we've already seen
              as we traverse the grid
        
        Algorithm:
        - Traverse the entire grid, row by row, column by column (O(m * n) runtime complexity)
        - At each cell, if water, continue
        - At each cell, if visited, continue
        - At each cell, if land, fully explore the island by visiting all connected components (O(m * n) runtime and space complexity)
          and increment count by 1
        - Return the total count
        """
        count = 0

        # simple edge case: nothing to explore!
        if not grid or not grid[0]:
            return count
        
        visited = set()
        directions = [
            (-1, 0), # up
            (+1, 0), # down
            (0, +1), # right
            (0, -1), # left
        ]

        def explore(r: int, c: int) -> bool:
            """
            Utility method to fully explore a given island.
            Returns false if the provided cell is not an island, or if the cell has already been visited.
            Otherwise, after exploring fully, returns true.
            """
            # verify that the cell is in-bounds
            if r < 0 or r >= len(grid):
                return False
            
            if c < 0 or c >= len(grid[0]):
                return False
            
            # verify that the cell is land
            if grid[r][c] == "0":
                return False
            
            # if the cell is seen, return early
            if (r, c) in visited:
                return False

            visited.add((r, c))

            for dr, dc in directions:
                explore(r + dr, c + dc)

            return True


        for r, row in enumerate(grid):
            for c, _ in enumerate(row):
                if explore(r, c):
                    count += 1

        return count