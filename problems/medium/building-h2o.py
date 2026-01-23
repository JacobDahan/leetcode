from threading import Semaphore, Barrier


class H2O:
    """
    There are two kinds of threads: oxygen and hydrogen. Your goal is to group these threads to form water molecules.

    There is a barrier where each thread has to wait until a complete molecule can be formed. 
    Hydrogen and oxygen threads will be given releaseHydrogen and releaseOxygen methods respectively, 
    which will allow them to pass the barrier. These threads should pass the barrier in groups of three, 
    and they must immediately bond with each other to form a water molecule. You must guarantee that 
    all the threads from one molecule bond before any other threads from the next molecule do.

    In other words:

        If an oxygen thread arrives at the barrier when no hydrogen threads are present, it must wait for two hydrogen threads.
        If a hydrogen thread arrives at the barrier when no other threads are present, it must wait for an oxygen thread and another hydrogen thread.

    We do not have to worry about matching the threads up explicitly; the threads do not necessarily know which other 
    threads they are paired up with. The key is that threads pass the barriers in complete sets; thus, if we examine 
    the sequence of threads that bind and divide them into groups of three, each group should contain one oxygen and 
    two hydrogen threads.

    Write synchronization code for oxygen and hydrogen molecules that enforces these constraints.
    """

    def __init__(self):
        """
        Task:
        - We are given a class H2O which is called variably by hydrogen and oxygen threads
        - We are asked to implement the hydrogen and oxygen threads such that oxygen and hydrogen calls must block
          until there are one and two threads waiting, respectively (forming a water molecule)
        
        Observations:
        - When we want threads to wait for a certain condition to be met, we can use a Condition lock from threading
        - However, a condition on its own is not sufficient: We need to unblock *two* hydrogens at once, based on the same condition
            - If we used a trivial condition (e.g., self.hydrogen_count >= 2), we would unlock ALL hydrogen calls at once
            - If we used a specific condition (e.g., self.hydrogen_count == 2), we could not handle a case like "HHHHHHHHHHOOOOO",
              as the hydrogens would not be released until long after the counter passed two
        
        Solution:
        - We can use semaphores to ensure that only two hydrogens and one oxygen (respectively) can advance at any one time
        - Since we are guaranteed by the semaphores that the combination of atoms is 3, we can use a trivial barrier to BLOCK
          the three threads until all are ready and present
        """
        self.hydrogens = Semaphore(2) # two hydrogens may advance at once
        self.oxygens = Semaphore(1) # only one oxygen may advance at one time
        self.molecule = Barrier(3) # two hydrogens plus one oxygen makes three atoms!


    def hydrogen(self, releaseHydrogen: 'Callable[[], None]') -> None:
            with self.hydrogens: # block until we can acquire the lock

                # there are a maximum of two hydrogens running at once here...

                self.molecule.wait()

                # if we've passed this check, we have two hydrogens and one oxygen, and the barrier is reset, blocking 
                # any other future threads from progressing

                # releaseHydrogen() outputs "H". Do not change or remove this line.
                releaseHydrogen()



    def oxygen(self, releaseOxygen: 'Callable[[], None]') -> None:
            with self.oxygens: # block until we can acquire the lock

                # there is a maximum of one oxygen running at once here...

                self.molecule.wait()

                # if we've passed this check, we have two hydrogens and one oxygen, and the barrier is reset, blocking 
                # any other future threads from progressing

                # releaseOxygen() outputs "O". Do not change or remove this line.
                releaseOxygen()
