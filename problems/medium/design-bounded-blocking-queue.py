from collections import deque
from threading import Lock, Condition

class BoundedBlockingQueue(object):
    """
    Implement a thread-safe bounded blocking queue that has the following methods:

    BoundedBlockingQueue(int capacity) The constructor initializes the queue with a maximum capacity.

    void enqueue(int element) Adds an element to the front of the queue. If the queue is full, the calling 
    thread is blocked until the queue is no longer full.

    int dequeue() Returns the element at the rear of the queue and removes it. 
    If the queue is empty, the calling thread is blocked until the queue is no longer empty.
    
    int size() Returns the number of elements currently in the queue.

    Your implementation will be tested using multiple threads at the same time. 
    Each thread will either be a producer thread that only makes calls to the enqueue method or a 
    consumer thread that only makes calls to the dequeue method. The size method will be called after every test case.
    """

    def __init__(self, capacity: int):
        """
        Task:
        - We are given an integer capacity and asked to create a bounded blocking queue of size capacity
        - The bounded blocking queue has a simple API:
            - enqueue: Add an element to the front of the queue; if the queue is full, block until no longer full
            - dequeue: Return the element at the rear of the queue and remove it; if the queue is empty, block until
              the queue is no longer empty
            - size: Return the number of elements in the queue
        
        Observations:
        - Every method against the queue needs to sit behind a lock; otherwise, the data could be mutated unsafely while
          accessed in another thread
        - Every time an element is enqueued or dequeued, we have to notify all tasks that the change has been made, in case
          a consumer was blocking waiting for the queue to have contents or a producer was waiting for the queue to have
          space
        - Distinct conditions are needed to determine whether consumers or producers (or neither) should be blocked
        - Taken together, this sounds like a good job for a condition lock

        Solution:
        - Use a condition lock where producers and consumers are blocked on a distinct condition (if either blocks)
            - For producers, acquire the lock and check if the queue is full; if it is, wait to be notified that there has
              been a state change, re-evaluate the state, and put the item to the queue
            - For consumers, acquire the lock and check if the queue is empty; if it is, wait to be notified that there has
              been a state change, re-evaluate the state, and remove the item from the queue
            - For preciseness, size should also require a lock. If we use a re-entrant lock in our condition lock, we can
              use this method to check the queue size when assessing conditions
        
        Optimization:
        - Use *two* conditions to control which threads we awake, but use the SAME inner lock to ensure we're always
          mutating the queue in only one thread at a time
            - When the queue is empty, we ONLY need to awake ONE consumer when we add ONE element to the queue
              (anything else is wasteful, and they'll go back to sleep after acquiring the lock!)
            - When the queue is full, we ONLY need to awake ONE producer when we remove ONE element from the queue
            - So long as we notify one consumer for every element we queue and one producer for every element we
              deque (since they only wait when full or empty!!!), we will minimize the wake-ups and the number of times
              the lock is unnecessarily picked up by threads that are guaranteed to not meet their condition
        """
        self.capacity = capacity
        self.lock = Lock()
        self.not_full = Condition(self.lock)
        self.not_empty = Condition(self.lock)
        self.queue = deque() # use a simple deque for O(1) push/pop operations
        

    def enqueue(self, element: int) -> None:
        with self.lock: # acquire the lock
            while len(self.queue) >= self.capacity: # the queue is full!
                self.not_full.wait() # wait to be told that something has changed
                # once we acquire the lock, here, we need to re-evaluate the capacity constraint
                # it's possible that we were spuriously awoken by the OS, or that another producer already
                # changed the state after we were notified
            
            # we have acquired the lock and the queue is not full, so add the element to the queue
            self.queue.append(element)

            # notify ONE consumer that we've added ONE element to the queue
            # (if the queue was empty, ONLY one consumer can actually do anything now; if the queue was not empty,
            #  there are no consumers waiting for a signal!)
            self.not_empty.notify()

    def dequeue(self) -> int:
        with self.lock: # acquire the lock
            while not self.queue: # the queue is empty!
                self.not_empty.wait() # wait to be told that something has changed
                # once we acquire the lock, here, we need to re-evaluate the capacity constraint
                # it's possible that we were spuriously awoken by the OS, or that another consumer already
                # changed the state after we were notified
            
            # we have acquired the lock and the queue is not empty, so remove the element from the queue
            val = self.queue.popleft()

            # notify ONE producer that we've removed something from the queue
            # (if the queue was not full, no producers will be waiting; if the queue was full, ONLY one can do anything now)
            self.not_full.notify()

            return val

    def size(self) -> int:
        with self.lock:
            return len(self.queue)