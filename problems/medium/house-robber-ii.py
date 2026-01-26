from typing import Dict, List

"""
You are a professional robber planning to rob houses along a street. Each house has a certain amount of money stashed. 

All houses at this place are arranged in a circle. That means the first house is the neighbor of the last one. 

Meanwhile, adjacent houses have a security system connected, and it will automatically contact the police if two adjacent houses were broken into on the same night.

Given an integer array nums representing the amount of money of each house, return the maximum amount of money you can rob tonight without alerting the police.
"""

class Solution:
    """
    Task:
    - We are given an array nums where nums[i] represents the money that can be obtained by robbing house i
    - Our task is to return the MAXIMUM amount of money that can be robbed from len(nums) houses
    - We have a CONSTRAINT that we MUST NOT rob adjacent homes
    - Additionally, the FIRST and LAST homes are considered adjacent, as this is a circular street

    Observations:
    - We are being asked to find the OPTIMAL (maximum) way to execute a task -- this immediately signals that we might consider a GREEDY algorithm
    - ... However, we have a constraint: Our decisions impact our ability to make future decisions
        - If we rob house i, we must not rob house i - 1 or house i + 1
        - We can prove that the greedy algorithm will not always be correct here (consider houses [6, 5, 1, 10] -- it is clearly optimal to rob 5 and 10, even though 6
          is locally optimal)
    - Additionally, we can define the problem generally to clarify that the problem is comprised of smaller sub-problems:
        - The most we can rob at the ith house (generally) := dp(i)
        - dp(i) = max(dp(i - 1), dp(i - 2) + nums[i]) // the most we can rob at the ith house is however much we could rob at the prior house, or the one before that, plus this one
    - Finally, we can see that there is clearly OVERLAP between these sub-problems: to solve for dp(i - 1), we must also solve for dp(i - 2), so we can benefit
      from caching the results of our sub-problem solutions to optimally solve our original problem
    
    Algorithm:
    - We can first consider the most basic case:
        - If the street was not circular...
            - dp(1) = nums[0] // the maximum robbable at the first house is the value of the first house
            - dp(2) = max(nums[0], nums[1]) // the maximum robbable at the second house is the maximum between the first two houses
            - We can use recursion down to these base cases to generally solve for any value i, and MEMOIZE our results
    - Because the street is circular...
        - Notice that the optimal solution must intuitively consist of EITHER robbing the first or last house, but never both
        - So, run our algorithm twice! Once for nums[:-1], once for nums[1:]
        - dp(1) = nums[0] // the maximum robbable at the first house is the value of the first house
        - dp(2) = max(nums[0], nums[1]) // the maximum robbable at the second house is the maximum between the first two houses
    - To solve this, we must:
        - Solve each sub-problem (almost) twice: Strictly O(2n) runtime, which we refer to as O(n)
        - Maximally, the stack depth will be of depth len(nums), resulting in O(n) space complexity; similarly, we must track a maximum of len(nums) results
          in our memoization table (O(2n) total space complexity, which can be simplified to O(n))
    - Once the recurrence relationship becomes clear, we can optimize to solve iteratively (reducing space complexity and risk of stack overflow for large inputs)

    Optimization:
    - Now that we understand the recurrence relationship, we can optimize our solution for space and eliminate the risk of stack overflow with exceptionally large inputs
    - Notice that each solution only depends on the prior two decisions
    - We do not need to memoize EVERY solution, we just need to track the immediately prior decisions
    - This will result in O(1) space complexity, while maintaining our O(n) runtime complexity (we still need to run two loops, evaluating each house in nums once --
      2n total iterations, which can be simplified to O(n))
    """
    def rob(self, nums: List[int]) -> int:
        if not nums:
            return 0 # nothing to rob!
        elif len(nums) == 1:
            return nums[0]

        # def rob_recursive(i: int, values: List[int], memo: Dict[int, int]) -> int:
        #     """
        #     Utility method for solving `rob` recursively. Returns the maximum amount robbable by the ith house (1-indexed).
        #     """
        #     if i in memo:
        #         return memo[i] # return the pre-computed value, where available

        #     if i == 1: # base case: we can maximally rob 0 at the first house
        #         return values[i - 1]
        #     elif i == 2: # base case: we can maximally rob max(nums[0], nums[1]) at the second house
        #         return max(values[i - 2], values[i - 1])

        #     result = max(rob_recursive(i - 1, values, memo), rob_recursive(i - 2, values, memo) + values[i - 1])
        #     memo[i] = result
        #     return result

        # return max(
        #     rob_recursive(len(nums) - 1, nums[:-1], dict()), # possible to rob the first house, ignore the last house
        #     rob_recursive(len(nums) - 1, nums[1:], dict()), # possible to rob the last house, ignore the first house
        # )

        def rob_iterative(start: int, end: int) -> int:
            """
            Utility method for optimally solving `rob` iteratively. Returns the maximum amount robbable between the bounds [start, end] (inclusive).
            """
            previous_result, previous_previous_result = 0, 0 # before we've reached any houses, we can't possibly have robbed anything of value!
            for i in range(start, end + 1):
                previous_result, previous_previous_result = max(previous_result, previous_previous_result + nums[i]), previous_result

            return previous_result

        # now that we've solved it recursively, we can improve our space complexity

        return max(
            rob_iterative(0, len(nums) - 2), # possible to rob the first house, ignore the last house
            rob_iterative(1, len(nums) - 1), # possible to rob the last house, ignore the first house
        )

import pytest 

@pytest.mark.parametrize(
    "nums,expected",
    [
        ([2,3,2], 3),
        ([1,2,3,1], 4),
        ([], 0),
        ([100], 100),
    ]
)
def test_rob(nums, expected):
    s = Solution()
    a = s.rob(nums)
    assert a == expected, f"Expected {expected}, received {a}"

if __name__ == "__main__":
    pytest.main(["-v", "-s"])