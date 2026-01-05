class Solution:
    def minCostClimbingStairs(self, cost: List[int]) -> int:
        """
        You are given an integer array cost where cost[i] is the cost of ith step on a staircase. 
        Once you pay the cost, you can either climb one or two steps.

        You can either start from the step with index 0, or the step with index 1.

        Return the minimum cost to reach the top of the floor.
        """
        # This question is asking us to find the MINIMUM cost to traverse a staircase
        # Questions that ask about minimum, maximum, or ways to do X are generally solved by greedy or DP algs
        # Furthermore, this question states that we can either climb one or two steps, meaning that certain choices
        # will impact other choices, and the local minimum (greedy) approach will not always be valid
        # This suggests that we should use DP

        # Are the conditions for DP met?
        # - At each step, we can find the minimum cost for climbing the remaining stairs from overlapping sub-
        #   problems (i.e., smaller versions of the problem that get re-used)
        # - Each of the sub-problems are optimal sub-components -- finding the optimal solution to the sub-problem
        #   gives us the optimal solution to the larger problem

        # So... let's use DP
        # - State: We only need to track the step that we are on (i)
        # - Recurrence relationship: The top of the stair-case can only be reached from the i-1 and i-2 stairs.
        #   In other words, the cost to reach the top of the stair-case is min(cost(i-1) + i-1, cost(i-2) + i-2).
        #   But what is the cost of any given step? It's simply the same: min(cost(i-1) + i-1, cost(i-2) + i-2).
        # - Base case: How can we solve for any cost without using DP? We are given that we can start from i = 0
        #   or i = 1, meaning the cost to reach those steps is 0 definitionally.
        
        # Bottom-Up (iterative):

        # If there are only two elements, the cost to top the stair-case is simply the cost of whichever
        # stair is cheaper
        if len(cost) <= 2:
            return min(cost)

        step_minus_one = 0
        step_minus_two = 0
        min_cost = 0

        for i in range(2, len(cost) + 1):
            # the minimum cost to REACH i is the minimum cost to REACH i-1 or i-2, plus the cost of that step
            min_cost = min(step_minus_one + cost[i - 1], step_minus_two + cost[i - 2])
            # as we move to the next iteration, the "previous" step becomes two behind, and the current min cost
            # becomes the previous
            step_minus_two = step_minus_one
            step_minus_one = min_cost
        
        return min_cost
    
        # # Top-Down (recursive):
        # memo = {}
        
        # def minCost(step: int) -> int:
        #     if step == 0 or step == 1:
        #         # Base cases: It costs nothing to reach steps at index 0 or 1, since we can start at either
        #         return 0
            
        #     # Check for step in memo
        #     if step not in memo:
        #         # If step doesn't exist, calculate it 
        #         # The cost to reach the step is equal to the minimum cost of reaching the prior steps, plus
        #         # the cost of those steps
        #         memo[step] = min(minCost(step - 1) + cost[step - 1], minCost(step - 2) + cost[step - 2])
            
        #     return memo[step]
        
        # We return minCost(len(cost)) because we treat the top of the staircase as its own step
        # The cost to reach this is simply the cost to reach any step we could reach it from, plus the cost of
        # that step (optimized)
        # return minCost(len(cost))
    
        # Test cases:
        # cost = [10,15,20]
        # --> minCost(3) --> min(minCost(2) + 20, minCost(1) + 15) --> min(minCost(0) + 10, minCost(1) + 15)
        # --> minCost(3) --> min(10 + 20, 0 + 15) --> return 15
        
