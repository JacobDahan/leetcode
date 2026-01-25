from typing import List

"""
You are a professional robber planning to rob houses along a street. 

Each house has a certain amount of money stashed, the only constraint stopping you from robbing each of them is that adjacent houses have security systems connected and it will automatically contact the police if two adjacent houses were broken into on the same night.

Given an integer array nums representing the amount of money of each house, return the maximum amount of money you can rob tonight without alerting the police.
"""

class Solution:
    """
    Task:
    - We are given an array nums where each num[i] represents the value that we can obtain by robbing the ith house
    - Our goal is to obtain the MAXIMUM value by robbing the OPTIMAL selection of homes, with the constraint that we
      MUST NOT rob adjacent homes

    Observations:
    - Our task is to find the OPTIMAL solution to a problem (often, this can be done with greedy or DP solutions)
    - The task has CONSTRAINTS whereby any decision impacts other decisions (we cannot rob house i + 1 if we robbed house i)
        - e.g., it is not always optimal to rob a house that has an apparently large value, as the next and prior homes may have a greater combined value
    - These conditions are generally suitable to be solved by DP, which gives us the CORRECTNESS of brute force and the SPEED of greedy algorithms
    - Is DP the right mechanism for solving this?
        - Generally, to solve the maximum amount we can rob at the ith house, we need to consider how much we could have robbed at PREVIOUS houses,
          plus the value of this house (i.e., the problem is comprised of repeating sub-problems)
        - Additionally, solving these sub-problems optimally will lead to the optimal solution for the ith house
    
    Algorithm:
    - Intuitively, we can define a recurrence relationship where dp(i) = max(dp(i - 1), dp(i - 2) + nums[i - 1])
        - In other words: The most money we can rob at the ith house is the most money we can rob by the i-1th house, or the i-2th house PLUS the value of the ith house
        - Base case: The maximum we can rob at the i = 0 (zeroth) house is trivially 0; the maximum at the i = 1 (first) house is trivially nums[0]
    - Therefore, we can start by writing this problem recursively and MEMOIZING partial solutions to avoid duplicate work
        - This will result in len(nums) non-memoized recursive calls (O(n) runtime complexity) (since retrieval and addition of memoized values is O(1) we do not include)
        - The call stack will therefore maximally be len(nums) in length (O(n) space complexity); similarly, we will maximally memoize len(nums) values
    
    Optimization:
    - While the recursive case is more intuitive, we can make two key observations:
        - With sufficiently large number of nums, the call stack may become to large and the program may crash (plus, recursion always has some runtime cost)
        - For each solution dp(i), we ONLY need to "know about" the i - 1 and i - 2 solutions; memoizing the entire solution space is unnecessary
    - To prevent stack overflow and reduce our space complexity, we can use an ITERATIVE approach (bottom-up) and TABULATION to solve this problem
        - We think about the problem the same way: The solution at dp[i] can be solved as the max(dp[i - 1], dp[i - 2] + nums[i - 1])
    """
    def rob(self, nums: List[int]) -> int:
        memo = dict()

        # edge case: empty or non-existent list has no value
        if not nums: 
            return 0

        def robRecursive(i: int) -> int:
            """
            Utility method to recursively solve the `rob` problem for the ith house.

            Results are memoized to reduce runtime complexity.
            """
            if i in memo: # if we have pre-computed the value, return early!
                return memo[i]
            
            if i <= 0: # base case: at the zeroth house, there's no value to obtain
                return 0
            elif i == 1: # base case: at the first house, we can maximally rob whatever the value of that house is
                return nums[0]

            # calculate the maximum we can rob at the ith house:
            # at house i, we can maximally make however much we could make by the prior house (impossible to rob this house), OR the house BEFORE THAT, plus robbing this house
            # recall: i = 0 represents the zeroth house, i = 1 represents the first house, and so on, so we need to adjust our indexing to read from nums
            result = max(robRecursive(i - 1), robRecursive(i - 2) + nums[i - 1])
            memo[i] = result # store the value for future calls
            return result

        def robIterative() -> int:
            """
            Utility method for optimized, iterative solution to the `rob` problem (same O(n) runtime, but faster without recursion).

            Results are tabulated, and only most recent two solutions are kept to reduce space complexity (O(1) space complexity).
            """
            if len(nums) == 1: # base case: if there's only one house, it's always optimal to rob
                return nums[0]
            
            obtained_by_prev_prev = 0 # dp[0]
            obtained_by_prev = nums[0] # dp[1]

            for i in range(1, len(nums)):
                maximum_obtained = max(obtained_by_prev_prev + nums[i], obtained_by_prev)
                obtained_by_prev_prev = obtained_by_prev
                obtained_by_prev = maximum_obtained
            
            return obtained_by_prev

        # return robRecursive(len(nums)) # first solution, then improve for interview to bottom-up!
        return robIterative()

import pytest

@pytest.mark.parametrize(
    "nums,expected",
    [
        ([1,2,3,1], 4),
        ([2,7,9,3,1], 12),
        ([], 0), # edge case: no homes to rob!
        ([1000], 1000), # edge case: one home to rob!
        ([5, 10, 6], 11), # sanity check: make sure we aren't running a greedy algo
    ]
)
def test_rob(nums, expected):
    s = Solution()
    a = s.rob(nums)
    assert a == expected, f"Expected {expected} but found {a}"

if __name__ == "__main__":
    pytest.main(['-v', '-s'])