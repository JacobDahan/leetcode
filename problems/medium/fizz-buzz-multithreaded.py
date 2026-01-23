from threading import Condition, Lock

class FizzBuzz:
    """
    You have the four functions:

        printFizz that prints the word "fizz" to the console,
        printBuzz that prints the word "buzz" to the console,
        printFizzBuzz that prints the word "fizzbuzz" to the console, and
        printNumber that prints a given integer to the console.

    You are given an instance of the class FizzBuzz that has four functions: fizz, buzz, fizzbuzz and number. The same instance of FizzBuzz will be passed to four different threads:

        Thread A: calls fizz() that should output the word "fizz".
        Thread B: calls buzz() that should output the word "buzz".
        Thread C: calls fizzbuzz() that should output the word "fizzbuzz".
        Thread D: calls number() that should only output the integers.

    Modify the given class to output the series [1, 2, "fizz", 4, "buzz", ...] where the ith token (1-indexed) of the series is:

        "fizzbuzz" if i is divisible by 3 and 5,
        "fizz" if i is divisible by 3 and not 5,
        "buzz" if i is divisible by 5 and not 3, or
        i if i is not divisible by 3 or 5.
    """

    def __init__(self, n: int):
        """
        Task:
        - We are given a class FizzBuzz that will be invoked (in some unknown order) to call fizz, buzz, fizzbuzz, and number
          by threads with a random scheduler
        - We are asked to print the FizzBuzz sequence up to the nth entry (1-indexed!!)

        Observations:
        - The first element printed is always a number (1)
        - With each element processed, we know what task needs to be awoken next
        - We can use a single lock to guarantee that only one thread advances at a time, and put that lock inside a condition
          to notify the NEXT waiting thread that it is time for that thread to advance
        - We can use multiple conditions to "surgically" awake threads and avoid needlessly taking the lock in threads
          that are guaranteed to fail their conditional check
        """
        self.n = n

        self.i = 1 # we always print 1 first, and we are given that 1 <= n
        self.lock = Lock() # use one lock to ensure one thread advances at a time

        # create a separate condition for each method so that we can "surgically" unblock threads
        self.fizz_next, self.buzz_next, self.fizzbuzz_next, self.number_next = Condition(self.lock), Condition(self.lock), Condition(self.lock), Condition(self.lock)


    # printFizz() outputs "fizz"
    def fizz(self, printFizz: 'Callable[[], None]') -> None:
    	while True:
            with self.lock: # first, acquire the lock
                # use a while loop to handle spurious wake-ups
                # since we surgically awake threads, there is no chance another thread "beats us to it" and changes this condition
                while self.i <= self.n and (self.i % 3 != 0 or self.i % 5 == 0): # "fizz" if i is divisible by 3 and not 5, otherwise wait
                    self.fizz_next.wait() # wait to be told that fizz is next
                    
                if self.i > self.n:
                    # we were awoken to shut down! exit
                    return

                # we've acquired the lock, so print fizz
                printFizz()

                # ... and increment our progress
                self.i += 1

                # notify the next task
                if self.notify_next():
                    return

    # printBuzz() outputs "buzz"
    def buzz(self, printBuzz: 'Callable[[], None]') -> None:
        while True:
            with self.lock: # first, acquire the lock
                # use a while loop to handle spurious wake-ups
                # since we surgically awake threads, there is no chance another thread "beats us to it" and changes this condition
                while self.i <= self.n and (self.i % 5 != 0 or self.i % 3 == 0): # "buzz" if i is divisible by 5 and not 3, otherwise wait
                    self.buzz_next.wait() # wait to be told that buzz is next
                    
                if self.i > self.n:
                    # we were awoken to shut down! exit
                    return

                # we've acquired the lock, so print buzz
                printBuzz()

                # ... and increment our progress
                self.i += 1

                # notify the next task
                if self.notify_next():
                    return

    # printFizzBuzz() outputs "fizzbuzz"
    def fizzbuzz(self, printFizzBuzz: 'Callable[[], None]') -> None:
        while True:
            with self.lock: # first, acquire the lock
                # use a while loop to handle spurious wake-ups
                # since we surgically awake threads, there is no chance another thread "beats us to it" and changes this condition
                while self.i <= self.n and (self.i % 3 != 0 or self.i % 5 != 0): # "fizzbuzz" if i is divisible by 3 and 5, otherwise wait
                    self.fizzbuzz_next.wait() # wait to be told that fizzbuzz is next
                    
                if self.i > self.n:
                    # we were awoken to shut down! exit
                    return

                # we've acquired the lock, so print fizzbuzz
                printFizzBuzz()

                # ... and increment our progress
                self.i += 1

                # notify the next task
                if self.notify_next():
                    return

    # printNumber(x) outputs "x", where x is an integer.
    def number(self, printNumber: 'Callable[[int], None]') -> None:
        while True:
            with self.lock: # first, acquire the lock
                # use a while loop to handle spurious wake-ups
                # since we surgically awake threads, there is no chance another thread "beats us to it" and changes this condition
                while self.i <= self.n and (self.i % 3 == 0 or self.i % 5 == 0): # "number" if i is not divisible by 3 nor 5, otherwise wait
                    self.number_next.wait() # wait to be told that number is next
                    
                if self.i > self.n:
                    # we were awoken to shut down! exit
                    return

                # we've acquired the lock, so print fizzbuzz
                printNumber(self.i)

                # ... and increment our progress
                self.i += 1

                # notify the next task
                self.notify_next()

    def notify_next(self):
        """
        Utility method to notify the next thread to advance.

        This MUST be called within the bounds of a held lock, else the behavior is undetermined.
        """
        if self.i > self.n:
            self.fizz_next.notify()
            self.buzz_next.notify()
            self.fizzbuzz_next.notify()
            self.number_next.notify()

        if self.i % 3 == 0 and self.i % 5 == 0:
            self.fizzbuzz_next.notify()
        elif self.i % 3 == 0:
            self.fizz_next.notify()
        elif self.i % 5 == 0:
            self.buzz_next.notify()
        else:
            self.number_next.notify()
