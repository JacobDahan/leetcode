from collections import deque

class RecentCounter:

    def __init__(self):
        self._counter = deque()

    def ping(self, t: int) -> int:
        self._counter.append(t)
        while (self._counter[0] < (t - 3000)):
            self._counter.popleft()
        
        return len(self._counter)


# Your RecentCounter object will be instantiated and called as such:
# obj = RecentCounter()
# param_1 = obj.ping(t)