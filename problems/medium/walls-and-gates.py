from collections import deque

class Solution:
    def wallsAndGates(self, rooms: List[List[int]]) -> None:
        """
        Do not return anything, modify rooms in-place instead.

        You are given an m x n grid rooms initialized with these three possible values.

        -1 A wall or an obstacle.
        0 A gate.
        INF Infinity means an empty room. We use the value 231 - 1 = 2147483647 to represent INF as you may assume that the distance to a gate is less than 2147483647.

        Fill each empty room with the distance to its nearest gate. If it is impossible to reach a gate, it should be filled with INF.
        """
        
        # Stupid approach: For each room, perform BFS to find the nearest gate
        # Naive approach: Find each gate; for each gate, perform BFS to all reachable rooms; update if shortest path
        # Smart approach: Perform multi-source BFS from all gates simultaneously

        queue = deque()
        seen = set()

        # First, find the gates (O(n))
        for y, row in enumerate(rooms):
            for x, room in enumerate(row):
                if room == 0:
                    # BFS uses a queue (first-in, first-out)
                    queue.append((y, x))
                    # Track the seen nodes to avoid cycles
                    seen.add((y, x))
        
        # Track the distance from nearest gate
        level = 0

        while queue:
            nodes_at_level = len(queue)
            for _ in range(0, nodes_at_level):
                y, x = queue.popleft()
                
                row = rooms[y]
                room = row[x]

                seen.add((y, x))

                # Do not process walls
                if room == -1:
                    continue

                # Only update distance if it's shorter
                if level < room:
                    rooms[y][x] = level
                
                # Add left neighbor
                if x > 0 and (y, x - 1) not in seen:
                    queue.append((y, x - 1))

                # Add right neighbor
                if x < len(row) - 1 and (y, x + 1) not in seen:
                    queue.append((y, x + 1))

                # Add up neigbor
                if y > 0 and (y - 1, x) not in seen:
                    queue.append((y - 1, x))

                # Add down neighbor
                if y < len(rooms) - 1 and (y + 1, x) not in seen:
                    queue.append((y + 1, x))
            
            level += 1
