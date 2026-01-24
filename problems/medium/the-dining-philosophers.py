from threading import BoundedSemaphore, Lock

class DiningPhilosophers:
    """
    Five silent philosophers sit at a round table with bowls of spaghetti. 
    Forks are placed between each pair of adjacent philosophers.

    Each philosopher must alternately think and eat. However, a philosopher can only eat spaghetti 
    when they have both left and right forks. Each fork can be held by only one philosopher and 
    so a philosopher can use the fork only if it is not being used by another philosopher. 
    After an individual philosopher finishes eating, they need to put down both forks so that the 
    forks become available to others. A philosopher can take the fork on their right or the one on 
    their left as they become available, but cannot start eating before getting both forks.

    The philosophers' ids are numbered from 0 to 4 in a clockwise order. 
    Implement the function void wantsToEat(philosopher, pickLeftFork, pickRightFork, eat, putLeftFork, putRightFork) where:

        philosopher is the id of the philosopher who wants to eat.
        pickLeftFork and pickRightFork are functions you can call to pick the corresponding forks of that philosopher.
        eat is a function you can call to let the philosopher eat once he has picked both forks.
        putLeftFork and putRightFork are functions you can call to put down the corresponding forks of that philosopher.

    Five threads, each representing a philosopher, will simultaneously use one object of your class to simulate the process. 
    The function may be called for the same philosopher more than once, even before the last call ends.
    """

    def __init__(self):
        self.philosophers = 5 # five philosophers
        self.forks = [Lock() for _ in range(self.philosophers)]
        self.diners = BoundedSemaphore(4) # bounded to avoid any accidental release leading to deadlock

    # call the functions directly to execute, for example, eat()
    def wantsToEat(self,
                   philosopher: int,
                   pickLeftFork: 'Callable[[], None]',
                   pickRightFork: 'Callable[[], None]',
                   eat: 'Callable[[], None]',
                   putLeftFork: 'Callable[[], None]',
                   putRightFork: 'Callable[[], None]') -> None:
        """
        Problem:
        - Five philosophers must share four forks to eat spaghetti
        - Each philosopher is separated by a fork around a circular table
        - A philosopher must have both a left and right fork to eat

        Task:
        - Design a concurrency algorithm wantsToEat such that the philosophers can continue alternating
        - The method may be called by multiple threads concurrently, with no set execution order or count

        Observations:
        - For any philosopher to eat, there are two locks (forks) he must acquire
        - If any philosopher acquires lock N, any other philosopher dependent on lock N must WAIT
        - Every philosopher N shares (left) fork N with philosopher (N - 1) % len(philosophers)
        - Every philosopher N shares (right) fork N + 1 with philosopher (N + 1) % len(philosophers)
        - Therefore, the left fork of every philosopher is the right of another, and vice versa for the left
        - To avoid deadlocks, philosophers MUST acquire locks in a set order:
            - Imagine two philosophers only (for simplicity)
            - The first takes the fork to his left (the right of the other)
            - The second takes the for to his left (the right of the first philosopher)
            - ... Now neither can advance! A classic deadlock! Both philosophers hold a resource that the other
              philosopher needs, and neither can force the other to release that resource or proceed without it
            - Instead, we must acquire forks (locks) consistently: The lower lock number is always acquired first
            - In the above scenario, the first philosopher takes fork 1 (to his left), and the second ALSO reaches for
              fork 1 (to his right), waiting until the first philosopher (now unblocked) eats with forks 1 and 2 to advance
        
        Optimization:
        - Here, we have all five philosophers concurrently attempting to eat
        - However, under high load, we have frequent lock contention and it's up to the OS scheduler to be "fair" and
          guarantee that no philosopher starves
        - We can take a small hit on peak concurrency by limiting our philosophers to eat *four* at a time
        - This reduces lock contention significantly and similarly guarantees that we can always advance
          (we can say that "there will always exist a philosopher to the right of another philosopher that is not eating" and
           therefore there is always a right fork available to avoid deadlocks)
        """
        # philosopher is zero-indexed, so consider fork zero to the left of philosopher zero
        # if this is the highest-numbered philosopher, his right fork is the same fork as fork zero (left of the first)
        left_fork, right_fork = philosopher, (philosopher + 1) % self.philosophers

        # only four diners may attempt to pick up forks at once
        with self.diners:
            # first, acquire the lower-numbered fork (always left, with our substitution above)
            with self.forks[left_fork]:
                # second, acquire the higher-numbered fork (always right, with our substitution above)
                with self.forks[right_fork]:
                    pickLeftFork()
                    pickRightFork()
                    eat()
                    putRightFork()
                    putLeftFork()