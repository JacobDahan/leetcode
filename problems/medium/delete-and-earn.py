class Solution:
    def deleteAndEarn(self, nums: List[int]) -> int:
        """
        You are given an integer array nums. 
        You want to maximize the number of points you get by performing the following operation any number of times:

        Pick any nums[i] and delete it to earn nums[i] points. 
        Afterwards, you must delete every element equal to nums[i] - 1 and every element equal to nums[i] + 1.

        Return the maximum number of points you can earn by applying the above operation some number of times.
        """
        # - We are given an integer array and told to find the MAXIMUM (i.e., optimal) way of performing some
        #   operations (implies greedy algo or DP)
        # - We are told that for any number n that we pick, we cannot pick any numbers n - 1 or n + 1
        # - When decisions impact other decisions, greedy algorithms fail
        # - Thus, this should be solved with DP

        # Note: If we take one of any element, we should take all of that element, since there is no further
        # cost to taking it. Therefore, we can group all of the duplicates together and store the "total benefit"
        # of taking any number.
        sums = {}
        max_num = 0

        for n in nums:
            if n in sums:
                sums[n] += n
            else:
                sums[n] = n
            max_num = max(max_num, n)

        # Is this a good problem for DP?
        # - Solving for n can be broken down into smaller, overlapping sub-problems
        # - The optimal solution for each sub-problem will yield the optimal solution for the greater problem
        
        # So what is the recurrence relationship (the relationship between one state and others)?
        # - For any index i, we can say only take nums[i] if we did not take nums[i - 1]
        # - So, the maximum value we can have if we take nums[i] is our maximum value at i - 2, plus nums[i]
        # - The maximum value we can have without nums[i] is our maximum value at i - 1
        # - Therefore, the optimal choice (whether to take index i or not) is simply:
        # max(dp[i - 1], dp[i - 2] + sums[i])

        ### Standard DP
        # dp = [0] * (max_num + 1) # create array with index bounds [0, max_num]

        # # Base cases:
        # # - The maximum we can get from taking zeros is... zero, so dp[0] = 0
        # # - The best we can do in any two-element array of ones and zeros is always going to be taking ones,
        # #   so the maximum we can get will be the number of ones (dp[1] = sums.get(1, 0))
        # dp[0] = 0
        # dp[1] = sums.get(1, 0)

        # for i in range (2, max_num + 1): # iterate over [2, max_num]
        #     dp[i] = max(dp[i - 1], dp[i - 2] + sums.get(i, 0))
        
        # return dp[-1]

        ### Improved DP
        # Because the recurrence relationship only depends on two elements, we don't need to store a full array
        # (that may have many empty elements)
        # Instead, we can just track the previous two answers...
        dp_minus_two = 0 # base case: dp[0]
        dp_minus_one = sums.get(1, 0) # base case: dp[1]
        prev = 1 # the last element we solved for (dp minus one)

        for n in sorted(sums.keys()): # iterate over [2, max_num]
            if n == 1:
                continue # already handled base case
            
            if n - prev == 1: # standard recurrence relationship...
                max_result = max(dp_minus_two + sums.get(n, 0), dp_minus_one)
            else: # more than one away from the previous, always best to take greedily...
                max_result = dp_minus_one + sums.get(n, 0)
            
            prev = n
            dp_minus_two = dp_minus_one # now i - 2 becomes i - 1
            dp_minus_one = max_result # and i becomes i - 1
        
        return dp_minus_one