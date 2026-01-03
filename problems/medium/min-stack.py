class MinStack:

    def __init__(self):
        self.stack = []
        self.mins = []

    def push(self, val: int) -> None:
        # First, append the new value
        self.stack.append(val)
        # Next, store the new minimum (if exists)
        if not self.mins:
            # If no previous exists, this is definitionally minimum
            self.mins.append((val, 1))
        elif val < self.mins[-1][0]:
            # We define a new minimum as any value that is greater than the previous minimum
            self.mins.append((val, 1))
        elif val == self.mins[-1][0]:
            # Val must be equal to the minimum
            self.mins[-1] = (self.mins[-1][0], self.mins[-1][1] + 1)

    def pop(self) -> None:
        if self.stack:
            val = self.stack.pop()
            min_val, min_count = self.mins[-1]
            if val == min_val and min_count == 1:
                self.mins.pop()
            elif val == min_val:
                self.mins[-1] = (val, min_count - 1)

    def top(self) -> int:
        return self.stack[-1]

    def getMin(self) -> int:
        return self.mins[-1][0]
        


# Your MinStack object will be instantiated and called as such:
# obj = MinStack()
# obj.push(val)
# obj.pop()
# param_3 = obj.top()
# param_4 = obj.getMin()