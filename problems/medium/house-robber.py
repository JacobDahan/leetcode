class Solution:
    def rob(self, nums: List[int]) -> int:
        """
        You are a professional robber planning to rob houses along a street. 
        Each house has a certain amount of money stashed, the only constraint 
        stopping you from robbing each of them is that adjacent houses have 
        security systems connected and it will automatically contact the 
        police if two adjacent houses were broken into on the same night.

        Given an integer array nums representing the amount of money of each 
        house, return the maximum amount of money you can rob tonight without 
        alerting the police.
        """

        # - This question is asking us to find a MAXIMUM
        # - This implies that we want to use a greedy algorithm or dynamic programming
        # - Further, this question demands that each decision take into account OTHER decisions
        #   (i.e., we can't rob house n if we also want to rob n+1 or if we already robbed n-1)
        # - Therefore, a greedy algorithm will not yield the best results, and we must use dynamic programming

        # - Will DP work?
        #   - This problem is comprised of overlapping sub-problems -- the optimal solution for n houses
        #     comprises the decision for n-1 and n-2 houses
        #   - This problem has an optimal substructure -- the optimal solution for n-1 and n-2 give us the optimal
        #     solution for n

        # - What do we need for DP?
        #   - The recurrence relation: How does the solution for n relate to the state for other solutions?
        #       - The decision for whether to rob house n is effectively: Is it better to rob n-2 + n or n-1?
        #   - The base case: What can we answer WITHOUT dynamic programming?
        #       - If there is one house, it is always best to rob that house
        #       - If there are two houses, it is always best to rob whichever gives more money
        if len(nums) == 1:
            return nums[0]
        elif len(nums) == 2:
            return max(nums[0], nums[1])
        
        dp = [0] * (len(nums) + 1)
        dp[1] = nums[0] # base case, if there is one house, it's always optimal to rob
        dp[2] = max(nums[0], nums[1]) # base case, if there are two houses, rob whichever has more money
        
        for i in range(3, len(nums) + 1):
            if_robbed = dp[i - 2] + nums[i - 1] # the amount of money robbed up to (excluding) the prior house,
                                                # plus the money from robbing this house
            if_not_robbed = dp[i - 1] # the amount of money robbed up to (including) the prior house
            dp[i] = max(if_robbed, if_not_robbed)

        
        return dp[len(nums)]
    
        # We can also solve this recursively, though this is less efficient, even with memoization
        # memo = {}
        # def robRecursiveDP(house: int) -> int:
        #     if house == 1:
        #         return nums[0]
        #     elif house == 2:
        #         return max(nums[0], nums[1])
            
        #     if not house in memo:
        #         if_robbed = robRecursiveDP(house - 2) + nums[house - 1]
        #         if_not_robbed = robRecursiveDP(house - 1)
        #         memo[house] = max(if_robbed, if_not_robbed)
            
        #     return memo[house]
        
        # return robRecursiveDP(len(nums))
        
        # Test cases:
        # - nums = [1,2,3,1] -> 4
        # --> dp[0] = 0
        # --> dp[1] = 1
        # --> dp[2] = 2
        # --> dp[3] = max(dp[1] + 3, dp[2]) = max(1 + 3, 2) = 4
        # --> dp[4] = max(dp[2] + 1, dp[3]) = max(2 + 1, 4) = 4
        # - nums = [2,7,9,3,1] -> 12
        # --> dp[0] = 0
        # --> dp[1] = 2
        # --> dp[2] = 7
        # --> dp[3] = max(dp[1] + 9, dp[2]) = max(2 + 9, 7) = 11
        # --> dp[4] = max(dp[2] + 3, dp[3]) = max(7 + 3, 11) = 11
        # --> dp[5] = max(dp[3] + 1, dp[4]) = max(11 + 1, 11) = 12