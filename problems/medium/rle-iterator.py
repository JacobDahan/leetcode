from collections import deque

class RLEIterator:

    def __init__(self, encoding: List[int]):
        # Use a deque for cheap popleft/pushleft operations
        self._encoding = deque(encoding)

    def next(self, n: int) -> int:
        next = -1
        while n > 0 and len(self._encoding) > 1:
            count, next = self._encoding.popleft(), self._encoding.popleft()

            if n < count:
                # If we haven't exhausted the value, put it back in the arr
                self._encoding.appendleft(next)
                self._encoding.appendleft(count - n)
            elif n > count:
                # If we have gone beyond the value, reset next to -1
                # (This will be properly set on the next go-around if possible)
                next = -1

            # Update the remaining n
            n -= count
        return next
        


# Your RLEIterator object will be instantiated and called as such:
# obj = RLEIterator(encoding)
# param_1 = obj.next(n)