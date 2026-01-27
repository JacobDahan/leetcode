from typing import List, Tuple

"""
Given an integer array nums, return the length of the longest strictly increasing subsequence.
"""

class Solution:
    """
    Task:
    - We are given an integer array nums and asked to return the LONGEST strictly increasing subsequence
    - A subsequence is NOT a sub-array, it does not need to be a contiguous
    - For example, in [1, 4, 2, 3], the longest increasing subsequence is [1, 2, 3], despite the 4 in the middle

    Observations:
    - We are asked to find the LONGEST (optimal) way to satisfy a certain condition
    - When we are asked to optimize something, we should think of GREEDY and DP approaches
    - ... However, this problem has a constraint: Every element we select may disallow selecting others (e.g., selecting 3 in the above example)
    - When decisions impact other decisions, greedy approaches are provably wrong (see again the example above)
    - Therefore, we need to consider using DP
    - How can we use DP?
        - Problem definition/restatement: We can restate the problem as (generically) "what is the longest substring I can form at index i of nums"
        - Restated, we can observe a recurrence relationship: dp[i] = max(dp[j] + 1, 1) for all j, j < i, nums[j] < nums[i]
        - In other words: We can solve for i by first solving for each of the preceeding elements of the array
        - This means that we will have to check (up to) the entire array on each iteration (n elements) while we iterate over all n elements
        - Therefore, we have a runtime complexity of O(n^2)
        - Similarly, we have a space complexity of O(n), since we must create the dp array of size n
    
    Algorithm:
    - I will first solve this recursively to make the recurrence algorithm obvious
        - I will create a helper function helper(start) that returns the maximum length subsequence up to index start
        - I will then memoize the helper function to reduce the runtime complexity from O(n^n) to O(n^2)
    - Time allowing, I can refactor this solution to an iterative solution that will be faster than the recursive one because it avoids
      the time cost of recursion and safer than the recursive one for large inputs by avoiding stack overflow (same overally time and space complexities)
    """

    def lengthOfLIS(self, nums: List[int]) -> int:
        if not nums:
            return 0

        # memo = dict()

        # def lis_recursive(end: int) -> int:
        #     """
        #     Utility method to recursively find the longest increasing subsequence up to and including the end index.
        #     """
        #     if end in memo:
        #         return memo[end]

        #     if end == 0: # base case, the longest subsequence we can make is always at least 1 -- the element itself!
        #         return 1
            
        #     lis = 1 # again, the LIS is minimally one, even if this is the smallest element in the array

        #     for i in range(end):
        #         if nums[end] > nums[i]:
        #             # remember what dp(i) means: the LIS terminating at i; if end < j, then the LIS does not terminate at end and we can't update end
        #             # we can only add ourselves to this LIS if we are greater than the value at i
        #             lis = max(lis_recursive(i) + 1, lis)
        #         else:
        #             # we still need to memoize the result so that we can check it later...
        #             _ = lis_recursive(i)
            
        #     memo[end] = lis
        #     return lis
        
        # lis = lis_recursive(len(nums) - 1)

        # for v in memo.values():
        #     lis = max(v, lis)
        
        # return lis

        # now that we've thoroughly explored the problem space, we can re-implement this as iterative, avoiding the overhead of recursion and the risk of stack overflow
        
        dp = [1] * len(nums) # the LIS is minimally one, even if this is the smallest element in the array
        
        for i, lis_i in enumerate(dp):
            for j in range(i):
                if nums[i] > nums[j]: # if i <= j, the subsequence at j must not terminate at i and we cannot update i
                    lis_i = max(dp[j] + 1, lis_i)
            
            dp[i] = lis_i
        
        return max(dp) # the LIS may not terminate at the last element! this is another O(n) operation

import pytest

@pytest.mark.parametrize(
    "nums,expected",
    [
        ([10,9,2,5,3,7,101,18], 4),
        ([0,1,0,3,2,3], 4),
        ([7,7,7,7,7,7,7], 1),
        ([7,7,7,7,7,7,7], 1),
        ([], 0),
        ([1], 1),
        ([1,4,2,3], 3),
        ([1,3,6,7,9,4,10,5,6], 6),
    ]
)
def test_longest_increasing_subseq(nums, expected):
    s = Solution()
    a = s.lengthOfLIS(nums)
    assert a == expected, f"Expected {expected}, observed {a}"

if __name__ == "__main__":
    pytest.main(['-v', '-s'])