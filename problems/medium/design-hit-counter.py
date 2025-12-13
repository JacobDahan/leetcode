class HitCounter:

    def __init__(self):
        self._counter = []
        
    # Records a hit that happened at timestamp (in seconds). 
    # Several hits may happen at the same timestamp.
    # In other words, we are receiving a SORTED list of timestamps.
    # Store it as such to make `get` calls fast.
    # Appending to the list is O(1) amortized and requires O(N) memory.
    def hit(self, timestamp: int) -> None:
        self._counter.append(timestamp)

    # Returns the number of hits in the past 5 minutes from timestamp (i.e., the past 300 seconds).
    # Specifically, for timestamp N, only hits at timestamp M (M >= N - 300) are included.
    def getHits(self, timestamp: int) -> int:
        left, right = 0, len(self._counter) - 1
        target_ts = timestamp - 300
        while left <= right:
            idx = (left + right) // 2
            ts = self._counter[idx]
            if ts <= target_ts:
                # Timestamp falls out of our search window
                left = idx + 1
            else:
                # Timestamp is within our search window
                right = idx - 1

        return len(self._counter) - left
        


# Your HitCounter object will be instantiated and called as such:
# obj = HitCounter()
# obj.hit(timestamp)
# param_2 = obj.getHits(timestamp)