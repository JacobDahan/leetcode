from collections import deque

class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        # Naive idea:
        # - Run BFS for each element in the grid
        # - Because we run for each element and stop when we meet water, any *new* land must be a new island
        # - If we have seen the land, continue
        islands = 0
        seen = set()
        queue = deque()

        def bfs():
            while queue:
                x, y = queue.popleft()

                if (x, y) in seen:
                    continue

                seen.add((x, y))

                if grid[y][x] == "0":
                    continue

                # Now queue all its neighbors
                if x > 0:
                    queue.append((x - 1, y))
                if x < len(grid[y]) - 1:
                    queue.append((x + 1, y))
                if y > 0:
                    queue.append((x, y - 1))
                if y < len(grid) - 1:
                    queue.append((x, y + 1))


        for y, row in enumerate(grid):
            for x, square in enumerate(row):
                if square == "1" and (x, y) not in seen:
                    islands += 1
                    queue.append((x, y))
                    bfs()

        
        return islands