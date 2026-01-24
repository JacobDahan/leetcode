from collections import OrderedDict

class Logger:
    """
    Design a logger system that receives a stream of messages along with their timestamps. 
    Each unique message should only be printed at most every 10 seconds (i.e. a message printed 
    at timestamp t will prevent other identical messages from being printed until timestamp t + 10).

    All messages will come in chronological order. Several messages may arrive at the same timestamp.

    Implement the Logger class:

        Logger() Initializes the logger object.
        bool shouldPrintMessage(int timestamp, string message) Returns true if the message should be printed in the given timestamp, otherwise returns false.
    """

    def __init__(self):
        """
        Task:
        - We are asked to implement shouldPrintMessage to return a boolean determining if a message should be logged
        - Messages should be logged IFF the SAME message has not been logged in the last 10s

        Observations:
        - We could trivially create a map of "recorded messages"
            - For each message, check if we've logged it by checking the map
            - If we have, check the last timestamp we've logged it
            - If the timesstamp >10s old, update the timestamp and log the message
            - Otherwise, log nothing!
            - If the message hasn't been recorded, record and log it... (O(1) check and O(m) insert, where m = len(message))
        - ... But, this means we'll never evict messages that are logged just once!
            - We achieve O(1) runtime complexity by accepting unbounded memory usage
        - We could instead use an time-ordered queue
            - For each message, clear out all the least recently used elements where last usage was >10s
                - In the worst case, each message comes in >10s after the next, meaning that we have to evict on every
                  call -- but we still only need to evice once for every call, so O(1) amortized!
            - For each message, check if it exists in the cache (O(1) runtime complexity)
            - If it exists, it MUST not be stale (since we just evicted the stale entries), so do not log
            - If it doesn't exist, insert into the cache and log
        """
        self.queue = OrderedDict()

    def shouldPrintMessage(self, timestamp: int, message: str) -> bool:
        self._evict(timestamp) # first, evict any stale records
        
        if message in self.queue:
            return False # we just evicted stale records; if the message is STILL in the cache, we should not log
        
        # __set_item__ for non-existent keys moves the value to the end of the list by default, so no need to do this manually
        self.queue[message] = timestamp # this gets hashed on our behalf anyways, no need to manually hash and store
        return True

    def _evict(self, now: int) -> None:
        # the queue is ordered from [oldest, ..., newest]
        # queue iterables are *views* that lock mutation, so just count how many pops we need to make
        expired_items = 0

        for timestamp in self.queue.values():
            if now - timestamp >= 10:
                expired_items += 1
            else:
                break # since we iterate from oldest to newest, all records after the FIRST non-expired will ALSO be non-expired 
        
        for _ in range(expired_items):
            self.queue.popitem(last=False)

# Your Logger object will be instantiated and called as such:
# obj = Logger()
# param_1 = obj.shouldPrintMessage(timestamp,message)