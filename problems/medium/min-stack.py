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
            self.mins.append(val)
        elif val <= self.mins[-1]:
            # We define a new minimum as any value that is equal to or greater than the previous minimum
            self.mins.append(val)

    def pop(self) -> None:
        if self.stack:
            val = self.stack.pop()
            if val == self.mins[-1]:
                self.mins.pop()

    def top(self) -> int:
        return self.stack[-1]

    def getMin(self) -> int:
        return self.mins[-1]
        


# Your MinStack object will be instantiated and called as such:
# obj = MinStack()
# obj.push(val)
# obj.pop()
# param_3 = obj.top()
# param_4 = obj.getMin()