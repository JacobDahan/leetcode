from collections import deque

class Solution:

    # In an infinite chess board with coordinates from -infinity to +infinity, you have a knight at square [0, 0].
    # A knight has 8 possible moves it can make, as illustrated below. 
    # Each move is two squares in a cardinal direction, then one square in an orthogonal direction.
    # Return the minimum number of steps needed to move the knight to the square [x, y]. 
    # It is guaranteed the answer exists.
    def minKnightMoves(self, x: int, y: int) -> int:
        # Thinking:
        # - We want to "search" for a path
        # - We want to return the *shortest* path
        # - BFS is best used for finding shortest path in an unweighted graph

        # How do we do BFS?
        # - We use a FIFO queue to track what places to visit next
        # - That is, for each node until we find our destination, we add each of its neighbors 
        #   to the back of the queue (those that require moves = n + 1)
        # - This way, we process all those squares that require moves = n first
        # - To ensure we don't get into recursive hell, we track what squares we have visited
        # - Since we are going move by move, if we've already visited a node, we know it won't be a faster
        #   trajectory back to the destination square, and we can abandon this branch entirely
        
        # BFS queue
        queue = deque()
        visited = set()

        queue.append((0, 0, 0))

        while len(queue) > 0:
            # Pop left to ensure FIFO ordering
            start_x, start_y, start_moves = queue.popleft()

            # If we found our spot, return the moves!
            if start_x == x and start_y == y:
                return start_moves

            # Otherwise, add each of the next moves to the queue
            moves = [
                (start_x - 1, start_y + 2),
                (start_x + 1, start_y + 2),
                (start_x + 2, start_y + 1),
                (start_x + 2, start_y - 1),
                (start_x + 1, start_y - 2),
                (start_x - 1, start_y - 2),
                (start_x - 2, start_y - 1),
                (start_x - 2, start_y + 1),
            ]

            for move in moves:
                # Only queue unvisited nodes
                if move not in visited:
                    visited.add(move)
                    move_x, move_y = move
                    # Append the current moves by 1
                    queue.append((move_x, move_y, start_moves + 1))
        
        # Unreachable
        return -1
    