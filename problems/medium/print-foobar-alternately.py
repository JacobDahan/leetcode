from threading import Condition

class FooBar:
    """
    The same instance of FooBar will be passed to two different threads:

    thread A will call foo(), while
    thread B will call bar().

    Modify the given program to output "foobar" n times.
    """

    def __init__(self, n):
        """
        Task:
        - We are given an integer n
        - Two threads will invoke foo() and bar() with no particular order
        - We must print "foobar" n times (no white space needed)

        Observations:
        - Regardless of the calling order, we must always execute foo(), then bar()
        - In other words, the thread calling bar() must sleep until execution of foo() is complete, and the thread calling
          foo() must sleep until execution of bar() is complete
        - We need to be careful not to reach a deadlock where foo() is awaiting bar() is awaiting foo()...
        - A simple condition can guarantee that the two threads "trade" control
            - Specifically, we can initialize a Condition with state is_foo = True
            - Both foo and bar can try to acquire the lock on the Condition
            - Foo will await is_foo = True (immediately true and set as such each iteration by bar)
            - Bar will await is_foo = False (set as such by foo)
            - There can never be a deadlock because foo and bar are waiting on diametrically opposed conditions!
        
        Solution:
        - Create a threading.Condition that is used as a gate for a boolean is_foo_next
        - Initialize is_foo_next to True
        - For each iteration i..n of foo, acquire the conditional lock
            - While is_foo_next is not true, release the conditional lock and await it to become true
            - To avoid erroneously unlocking, use a while loop to reassert the condition with lock acquired
            - print foo
            - set is_foo_next to false
        - For each iteration i..n of bar, acquire the conditional lock
            - While is_foo_next is true, release the conditional lock and await it to become false
            - To avoid erroneously unlocking, use a while loop to reassert the condition with lock acquired
            - print bar
            - set is_foo_next to true
        """
        self.n = n

        # a condition is a thin wrapper around a Lock that enables us to wait not for the lock to be free,
        # but a condition to evaluate to True (and then to acquire a lock...)
        self.condition = Condition()

        # this is the actual boolean that is evaluated with each conditional check
        # it is NOT safe to modify this boolean outside of any domain where the condition lock is acquired
        self.is_foo_next = True

    def foo(self, printFoo: 'Callable[[], None]') -> None:
        
        for i in range(self.n):
            
            with self.condition: # we need to re-acquire the lock on the condition
                while not self.is_foo_next: # use while in case the OS erroneously releases the underlying lock
                    self.condition.wait()

                # printFoo() outputs "foo". Do not change or remove this line.
                printFoo()

                # next is bar
                self.is_foo_next = False
                self.condition.notify() # wake up the bar task!


    def bar(self, printBar: 'Callable[[], None]') -> None:
        
        for i in range(self.n):
            
            with self.condition: # we need to re-acquire the lock on the condition
                while self.is_foo_next: # use while in case the OS erroneously releases the underlying lock
                    self.condition.wait()
                    
                # printBar() outputs "bar". Do not change or remove this line.
                printBar()

                # next is foo
                self.is_foo_next = True
                self.condition.notify() # wake up the foo task!