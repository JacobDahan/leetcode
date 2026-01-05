class Solution:

    def __init__(self):
        self.memo = {}

    def climbStairs(self, n: int) -> int:
        """
        You are climbing a staircase. It takes n steps to reach the top.
        Each time you can either climb 1 or 2 steps. 
        In how many distinct ways can you climb to the top?
        """
        # - This is a "how many" type question
        # - Maximum/minimum/longest/shortest/how many questions are a quiet indicator that we need to use a 
        #   greedy or dynamic programming approach
        # - Each time that we choose one or two steps, we implicitly remove the ability to choose the other (if 
        #   we choose 2, we hop past 1)
        # - This need to take into account other decisions when making a decision implies greedy will not work
        # - We also see that each problem is composed of overlapping sub-problems (how many ways to step n
        #   is highly dependent on work done to answer the question for n-1, n-2, etc.)
        # - Finally, we see that there is an optimal sub-structure (the optimal solution to the problem can be
        #   constructed from optimal solutions to its sub-problems)
        # - This implies that we can use dynamic programming to solve this problem

        # Now, for DP, we can solve this top-down (recursion) or bottom-up (iterative)
        # Because n may only be of size 45, it does not really matter... But we will do both for practice

        # Recursive:
        # return self.dpRecursive(n)
    
        # Iterative:
        return self.dpIterative(n)

    def dpRecursive(self, n: int) -> int:
        # - How many ways can we reach step n?
        # - We must have reached n by step n-1 or step n-2 (since we can only move in one step or two)
        # - Therefore, the number of ways to reach n is simply the number of ways to reach n-1, plus the number
        #   of ways to reach step n-2
        #   (Consider n=3; we must have reached from n=1 (one way to reach) or n=2 (two ways to reach), so there are 
        #   3 routes -- 1-->1-->1; 1-->2; 2-->1)
        # - Formally, we can say that dpRecursive(n) = dpRecursive(n-1) + dpRecursive(n-2)
        # - We also have simple base cases: There is 1 way to reach n=1, and 2 ways to reach n=2
        if n == 1 or n == 2:
            return n
        
        if n not in self.memo:
            self.memo[n] = self.dpRecursive(n-1) + self.dpRecursive(n-2)

        return self.memo[n]

    
    def dpIterative(self, n: int) -> int:
        # - As with the recursive formulation, we have base cases (1 way to reach n=1, 2 ways to reach n=2)
        #   and we know that f(n) = f(n-1) + f(n-2)
        # - However, here we do not need to use memoization, and can instead use tabulation to build UP our answer
        if n == 1 or n == 2:
            return n
        
        # For raw DP:
        # tabulation = [0] * n
        # tabulation[0] = 1 # n = 1, we use n-1 indices
        # tabulation[1] = 2 # n = 2
        # for i in range(2, n):
        #     tabulation[i] = tabulation[i-1] + tabulation[i-2]
        
        # return tabulation[n-1]

        # In its optimized form:
        n_minus_1 = 2 # n = 2
        n_minus_2 = 1 # n = 1
        for _ in range(3, n):
            result = n_minus_1 + n_minus_2
            n_minus_2 = n_minus_1
            n_minus_1 = result
        
        return n_minus_1 + n_minus_2