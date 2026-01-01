class MovingAverage:

    def __init__(self, size: int):
        self.window = [0] * size
        self.count = 0
        self.head = 0
        self.sum = 0

    # 3, 1, 10, 3, 5
    # 3 --> head = 0, tail = 0, window = [3] --> 3 / 1 = 3.0
    # 3, 1 --> head = 0, tail = 1, window = [3, 1] --> (3 + 1) / 2 = 2.0
    # 3, 1, 10 --> head = 0, tail = 2, window = [3, 1, 10] --> (3 + 1 + 10) / 3 = 4.66667
    # 1, 10, 3 --> head = 1, tail = 0, window = [3, 1, 10] --> (1 + 10 + 3) / 3 = 4.66667
    # 10, 3, 5 --> head = 2, tail = 1, window = [5, 1, 10] --> (10 + 3 + 5) / 3 = 6.0
    def next(self, val: int) -> float:
        # First, find the index where the value should be inserted
        index = (self.head + self.count) % len(self.window)

        # Insert the value
        self.sum -= self.window[index]  # Remove the old value from the sum
        self.sum += val                 # Add the new value to the sum
        self.window[index] = val        # Update the window

        # Next, update the count
        # - Count can never be greater than len(self.window)
        # - If the count is equal to len(self.window), we must shift the head
        if self.count < len(self.window):
            # Until the count is equal to the window size, the head will not move
            self.count += 1
        else:
            # Once we have filled our queue, the head must move forwards (and wrap around)
            self.head = (self.head + 1) % len(self.window)

        return self.sum / self.count


# Your MovingAverage object will be instantiated and called as such:
# obj = MovingAverage(size)
# param_1 = obj.next(val)