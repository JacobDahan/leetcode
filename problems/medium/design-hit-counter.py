class HitCounter:

    def __init__(self):
        self._counter = []
        
    # Records a hit that happened at timestamp (in seconds). 
    # Several hits may happen at the same timestamp.
    # In other words, we are receiving a SORTED list of timestamps.
    # Store it as such to make `get` calls fast.
    # Appending to the list is O(1) amortized and requires O(N) memory.
    def hit(self, timestamp: int) -> None:
        if not self._counter:
            self._counter.append((timestamp, 1))
            return

        ts, c = self._counter[-1]
        if ts == timestamp:
            self._counter[-1] = (ts, c + 1)
            return
        
        self._counter.append((timestamp, 1))

    # Returns the number of hits in the past 5 minutes from timestamp (i.e., the past 300 seconds).
    # Specifically, for timestamp N, only hits at timestamp M (M >= N - 300) are included.
    def getHits(self, timestamp: int) -> int:
        left, right = 0, len(self._counter) - 1
        target_ts = timestamp - 300
        while left <= right:
            idx = (right - left) // 2 + left
            ts, _ = self._counter[idx]
            if ts <= target_ts:
                left = idx + 1
            else:
                right = idx - 1

        sum = 0
        while left < len(self._counter):
            sum += self._counter[left][1]
            left += 1

        return sum

# Your HitCounter object will be instantiated and called as such:
# obj = HitCounter()
# obj.hit(timestamp)
# param_2 = obj.getHits(timestamp)