from collections import deque
from threading import Condition, Lock

class BoundedBlockingQueue(object):
    """
    Implement a thread-safe bounded blocking queue that has the following methods:

      BoundedBlockingQueue(int capacity) The constructor initializes the queue with a maximum capacity.
      void enqueue(int element) Adds an element to the front of the queue. 
        If the queue is full, the calling thread is blocked until the queue is no longer full.
      int dequeue() Returns the element at the rear of the queue and removes it. 
        If the queue is empty, the calling thread is blocked until the queue is no longer empty.
      int size() Returns the number of elements currently in the queue.

    Your implementation will be tested using multiple threads at the same time. 
    Each thread will either be a producer thread that only makes calls to the enqueue method 
    or a consumer thread that only makes calls to the dequeue method. 
    The size method will be called after every test case.
    """

    def __init__(self, capacity: int):
        """
        Task:
        - We must implement a bounded blocking queue that enables multiple threads (scheduled in any order) to
          enqueue and dequeue integer elements
        - Producer threads should block if the queue is full, and consumer threads should block if the queue is empty

        Observations:
        - Any operations on the queue MUST be guarded behind a lock -- only one producer or consumer may safely add to
          or remove from the queue at any given time
        - When enqueing, if we find that the buffer is full, we must release the lock and wait for the state to change
        - When dequeuing, if we find that the buffer is empty, we must release the lock and wait for the state to change
        - When enqueing or dequeing, the state change we induce can MAXIMALLY impact one waiting thread
          - If we enqueue to an empty queue, we must not have waiting producers (no need to wait on empty queue) and
            ONLY ONE waiting consumer (if any) can actually take any action (since we only queued one element)
          - If we dequeue from a full queue, we must not have any waiting consumers (no need to wait on full queue) and
            ONLY ONE waiting producer (if any) can actually take any action (since we only created space for one element)
        - Therefore, we can use TWO conditions (one for producers and one for consumers) to "surgically" awake threads,
          reducing unecessary task switching for the OS and lock contention
        """
        self.capacity = capacity
        self.buffer = deque() # do NOT mutate this outside the bounds of an acquired lock, as dequeues are not thread safe
        self.lock = Lock()
        self.notify_producer = Condition(self.lock) # to notify ONE producer that the queue is no longer full
        self.notify_consumer = Condition(self.lock) # to notify ONE consumer that the queue is no longer empty

    def enqueue(self, element: int) -> None:
        with self.lock: # first, acquire the lock
            # use WHILE to ensure that the condition is re-evaluated on spurious wake-ups
            while len(self.buffer) >= self.capacity: # if the queue is full, wait to be notified that there is space
                self.notify_producer.wait()
            
            # we've acquired the lock and the buffer has space, queue the element
            self.buffer.append(element)

            # if there are any consumers that were stuck waiting for elements in the queue, notify ONE AND ONLY ONE
            self.notify_consumer.notify()

    def dequeue(self) -> int:
        with self.lock: # first, acquire the lock
            # use WHILE to ensure that the condition is re-evaluated on spurious wake-ups
            while not self.buffer: # if the queue is empty, wait to be notified that there is something to dequeue
                self.notify_consumer.wait()
            
            # we've acquired the lock and the buffer has an element, dequeue
            val = self.buffer.popleft()

            # if there are any producers that were stuck waiting for space in the queue, notify ONE AND ONLY ONE
            self.notify_producer.notify()
            
            return val

    def size(self) -> int:
        with self.lock: # first, acquire the lock
            return len(self.buffer)