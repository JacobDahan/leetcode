from typing import List

"""
You are given an integer array coins representing coins of different denominations and an integer amount representing a total amount of money.

Return the fewest number of coins that you need to make up that amount. If that amount of money cannot be made up by any combination of the coins, return -1.

You may assume that you have an infinite number of each kind of coin.
"""

class Solution:
    """
    Task:
    - We are given an array of coins coins where coins[i] is equal to the value of the ith coin
    - We are tasked to find the MINIMUM number of coins that equals EXACTLY the amount amount
    - If the amount of money cannot be made up, we return -1

    Observations:
    - If we think about how we would solve this problem, we might start with a greedy algorithm -- we are asked to find the minimum number of coins,
      and when we are asked to OPTIMIZE something, greedy algorithms are often very efficient
    - However, we can think of a case where a greedy algorithm (take the largest coin where coin[i] < amount) fails:
        - e.g., coins = [1, 4, 5], amount = 13 -- a greedy algorithm would take [5, 5, 1, 1, 1], but we could do better with [4, 4, 5]
    - Since a greedy algorithm will not be correct, let us reconsider the problem:
        - We can restate the problem as "what is the minimum number of coins to create amount i"
        - Then, to solve for i, we realize that we have only len(coins) choices: we can take any one of the coins available
        - Because this is a decision tree, and trees are naturally recursive, we might consider using recursion to solve this problem
        - As we look at the tree, we recognize that there are repeating sub-problems (for example, coins = [1, 2], amount = 10, we will need to solve for 8 twice, 7 thrice, and so on)
        - Additionally, we can see that the optimal solution to the original problem can be reached from the solutions of sub-problems
        - Together, this suggests that we can use DP
    
    Algorithm:
    - Recurrence relationship: dp(i) = min(dp(i - j)) + 1 for all j in coins, such that i - j >= 0
        - In other words: The minimum number of coins to generate amount i is equal to the minimum amount of coins to generate i - j, where j is the value of the 
          next selected coin, plus one (for selecting j!)
    - Base cases:
        - When i = 0, we require exactly 0 coins to generate the amount
        - When i < 0, we return -1 as it is impossible to generate the amount
    
    Complexity:
    - In the worst case, coins will be a list of 1s, and we will have to visit every amount between amount and 0
    - In this case, we will have n := amount iterations, wherein we need to check m := len(coins) sub-trees
    - However, because of our memoization, we only EVALUATE those sub-trees once; so we visit n values multiple times, but most operations are only O(1) lookups and arithmatic
    - Therefore, we have a time complexity of O(n * m) -- n iterations with m branches in each iteration
    - Because our call stack will maximally be n elements deep in the worst case, we have space complexity of O(n) (we also need to store maximally n entries in memo,
      which is also O(n) complexity, giving us a total of O(2n), which simplifies to the original O(n))
    
    Optimization:
    - Now that we've thoroughly explored the problem space, we might consider what happens if we have an exceptionally large amount (say, 10000)?
    - This would lead to stack overflow and serious recursion overhead
    - Instead, we can speed things up and eliminate overflow risk by re-factoring to ITERATIVELY BUILD UP our DP solution
    - We use the same (or similar) recurrence relation: dp[i] = min(dp[i - j]) + 1 for all j in coins, i - j > 0
    - We'll tabulate our results in an array where dp[i] represents the optimal solution to the problem "how many coins minimum do I need to return value i"
    """

    def coinChange(self, coins: List[int], amount: int) -> int:
        # memo = dict()

        # def coin_change_recursive(coins: List[int], amount: int, memo: dict) -> int:
        #     """
        #     Utility method for memoized recursive computation of coin change.
        #     Returns the minimum number of coins required to return amount using coins coins.
        #     """
        #     if amount in memo:
        #         return memo[amount]

        #     if amount == 0: # base case: it takes 0 coints to return amount 0
        #         return 0
            
        #     if amount < 0: # base case: it is not possible to return a negative amount
        #         return -1 

        #     if not coins: # impossible to generate non-zero amount with no coins!
        #         return -1
            
        #     num_coins = -1

        #     for coin in coins:
        #         num_coins_minus_one = coin_change_recursive(coins, amount - coin, memo)
        #         if num_coins_minus_one >= 0: # do not update if this branch returns no valid solutions
        #             if num_coins == -1: # anything is better than an invalid solution, so take this blindly
        #                 num_coins = num_coins_minus_one + 1 # add one for the coin we just choices
        #             else:
        #                 num_coins = min(num_coins, num_coins_minus_one + 1)
            
        #     memo[amount] = num_coins
        #     return num_coins
        
        # return coin_change_recursive(coins, amount, memo)

        # I'll keep the recursive solution to refer back to as I code, and also so that we can track progress

        # first, create our dp array
        # we're going to TABULATE our results as we go (make array size n + 1 to properly align to indexes and leave a slot at 0 for the true zero amount base case)
        dp = [-1] * (amount + 1) # use -1 as the "base case" since we know that's what we must return if it's not possible to satisfy the constraints

        # base case: if the amount is zero, we need no coins!
        dp[0] = 0

        for value_remaining in range(1, amount + 1):
            for coin in coins:
                if value_remaining - coin < 0: # we cannot use this coin, continue
                    continue
                
                dp_minus_coin = dp[value_remaining - coin] # fetch the minimum number of coins to reach the value one coin prior

                if dp_minus_coin < 0: # we cannot use this coin, as it cannot reach zero itself
                    continue
                
                if dp[value_remaining] == -1:
                    dp[value_remaining] = dp_minus_coin + 1
                else:
                    dp[value_remaining] = min(dp[value_remaining], dp_minus_coin + 1)
        
        return dp[-1]

import pytest 

@pytest.mark.parametrize(
    "coins,amount,expected",
    [
        ([1,2,5], 11, 3),
        ([2], 3, -1),
        ([1], 0, 0),
        ([1, 4, 5], 13, 3),
    ]
)
def test_coin_change(coins, amount, expected):
    s = Solution()
    a = s.coinChange(coins, amount)
    assert a == expected, f"Expected {expected}, observed {a}"

if __name__ == "__main__":
    pytest.main(['-v', '-s'])