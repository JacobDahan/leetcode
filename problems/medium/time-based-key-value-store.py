from collections import defaultdict

class TimeMap:

    def __init__(self):
        self._store = defaultdict(list)

    # All the timestamps timestamp of `set` are strictly increasing.
    # This means we can simply append (v, ts) pairs to the store
    # and keep the sorted order, enabling O(log_n) lookups at `get` time.
    def set(self, key: str, value: str, timestamp: int) -> None:
        self._store[key].append((value, timestamp))
        

    def get(self, key: str, timestamp: int) -> str:
        # First, we have a few edge cases to check...
        values = self._store[key]

        # If there's nothing in the store, return none
        if not values:
            return ""
        
        # Similarly, if the provided timestamp is lower than
        # the lowest stored, return none
        _, ts = values[0]
        if ts > timestamp:
            return ""
        
        # Lastly, if the provided timestamp is greater than
        # the greatest stored, return the associated value
        v, ts = values[-1]
        if ts <= timestamp:
            return v
        
        # If we still haven't returned, we need to run a binary
        # search to find the greatest lesser timestamp
        l = 0
        r = len(values)
        best_v = ""

        while l < r:
            # Our index is the mid-point between l and r, offset by l
            idx = ((r - l) // 2) + l
            possible_v, ts = values[idx]
            
            # If the ts is greater than the provided ts, we need to move to
            # the left, and can't us possible_v
            if ts > timestamp:
                r = idx
            # If the ts is less than the provided ts, we should look for a better
            # solution, but store the possible_v
            elif ts < timestamp:
                best_v = possible_v
                l = idx + 1
            # A perfect match!
            else:
                return possible_v
            
        return best_v