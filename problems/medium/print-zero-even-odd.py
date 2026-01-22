from threading import Condition

class ZeroEvenOdd:
    """
    You have a function printNumber that can be called with an integer parameter and prints it to the console.

    For example, calling printNumber(7) prints 7 to the console.

    You are given an instance of the class ZeroEvenOdd that has three functions: zero, even, and odd. 
    The same instance of ZeroEvenOdd will be passed to three different threads:

    Thread A: calls zero() that should only output 0's.
    Thread B: calls even() that should only output even numbers.
    Thread C: calls odd() that should only output odd numbers.

    Modify the given class to output the series "010203040506..." where the length of the series must be 2n.
    """

    def __init__(self, n):
        """
        Task:
        - We are given a "number printer" that we call to print x, where x is an integer
        - We are also given an integer n
        - Finally, we are given three methods to implement (zero, even, odd) that will be called by three distinct threads
          with no predictable execution order
        - We are asked to implement these methods such that they will (together) output a series "010203..."
          where the length of the series must be 2n
        
        Observations:
        - Effectively, we are being asked to print "zero", "odd", "zero", "even", ...
        - We can define a condition that dictates what method should execute next
            - Specifically, we can track the latest value we have printed, and if a zero should come next
            - Each time we print a zero, we should set zero_next to false
            - Each time we print a non-zero integer, we should increment the current value and set zero_next to true
            - Each of these methods should return when the current value is equal to n
        
        Notes:
        - We CANNOT modify the current value or zero_next outside of holding our condition lock, as this is not thread safe
        - When we acquire the condition lock, we must re-evaluate our condition to ensure there was no spurious awaking by
          the OS or that we are reading a signal destined for another condition lock
        """
        self.n = n
        self.current = 1 # the first non-zero integer should be 1
        self.zero_next = True # the first printed integer should be zero
        self.condition = Condition()
        
        
	# printNumber(x) outputs "x", where x is an integer.
    def zero(self, printNumber: 'Callable[[int], None]') -> None:
        for _ in range(self.n): # we print zero a total of n times
            with self.condition: # first, acquire the lock
                while not self.zero_next: # we need to re-check this condition when the wait is released, so use WHILE not IF
                    self.condition.wait()
                
                # now we own the condition lock, and we know zero_next is true, so print zero
                printNumber(0)

                # the next number should NOT be a zero
                self.zero_next = False

                # wake the sleeping threads to re-evaluate their conditions
                self.condition.notify_all()
        
    def even(self, printNumber: 'Callable[[int], None]') -> None:
        for _ in range(2, self.n + 1, 2): # we print even numbers a total of n / 2 times
            with self.condition: # first, acquire the lock
                while self.zero_next or self.current % 2: # if zero should be printed or the current value is not even, we have to wait
                    self.condition.wait()
                
                # now we own the condition lock, and we know the next value is even, so print it
                printNumber(self.current)

                # the next number should be a zero
                self.zero_next = True

                # ... and after that an odd number
                self.current += 1

                # wake the sleeping threads to re-evaluate their conditions
                self.condition.notify_all()

        
        
    def odd(self, printNumber: 'Callable[[int], None]') -> None:
        for _ in range(1, self.n + 1, 2): # we print odd numbers a total of n / 2 times
            with self.condition: # first, acquire the lock
                while self.zero_next or not self.current % 2: # if zero should be printed or the current value is not odd, we have to wait
                    self.condition.wait()
                
                # now we own the condition lock, and we know the next value is even, so print it
                printNumber(self.current)

                # the next number should be a zero
                self.zero_next = True

                # ... and after that an even number
                self.current += 1

                # wake the sleeping threads to re-evaluate their conditions
                self.condition.notify_all()
        