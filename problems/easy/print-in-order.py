from threading import Event

class Foo:
    """
    The same instance of Foo will be passed to three different threads. 
    
    Thread A will call first(), thread B will call second(), and thread C will call third(). 
    
    Design a mechanism and modify the program to ensure that second() is executed after first(), 
    and third() is executed after second().

    Note:
        We do not know how the threads will be scheduled in the operating system, even though the numbers in the input seem 
        to imply the ordering. The input format you see is mainly to ensure our tests' comprehensiveness.
    """

    def __init__(self):
        """
        Task:
        - We are asked to update Foo such that first(), second(), and third() will *execute* in that order, regardless
          of the order in which the calling threads are scheduled.

        Observations:
        - This is relatively simple if we use events -- we can await notification that the event has occurred
        - We just need to define an event for each task, and notify and waiting threads that the task is completed
        - (Alternatively, and equally, we could use two locks that both *start* as locked and are sequentially unlocked...)
        """
        self.first_completed = Event()
        self.second_completed = Event()


    def first(self, printFirst: 'Callable[[], None]') -> None:
        # as soon as first is called, it should be executed -- there is nothing blocking its execution
        # printFirst() outputs "first". Do not change or remove this line.
        printFirst()

        # make sure to notify any waiting threads that our work is done
        self.first_completed.set()


    def second(self, printSecond: 'Callable[[], None]') -> None:
        # wait for the first to be executed before proceeding
        self.first_completed.wait()

        # printSecond() outputs "second". Do not change or remove this line.
        printSecond()

        # make sure to notify any waiting threads that our work is done
        self.second_completed.set()


    def third(self, printThird: 'Callable[[], None]') -> None:
        # wait for the second to be executed before proceeding
        self.second_completed.wait()

        # printThird() outputs "third". Do not change or remove this line.
        printThird()