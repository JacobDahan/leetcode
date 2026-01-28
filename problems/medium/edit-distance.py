"""
Given two strings word1 and word2, return the minimum number of operations required to convert word1 to word2.

You have the following three operations permitted on a word:

    Insert a character
    Delete a character
    Replace a character

"""

class Solution:
    """
    Task:
    - We are given two strings (word1, word2) and asked to find the MINIMUM (optimal) operations to convert word1 to word2
    - We are only allowed to INSERT, DELETE, or REPLACE characters

    Observations:
    - We are asked to find the OPTIMAL (minimum) way to solve a problem; this suggests we may want to use dynamic programming
    - Before we can jump into DP, we need to think about how we would solve this problem by brute force
        - This will help us discover any repeating sub-problems
        - This will also help us discover the recurrence relationship, if one exists
    
    Brute force:
    - Given two strings, we would intuitively start comparing them character by character and building out a decision tree of what "edits" to make
    - At each index i, j in word1, word2, we can intuitively say that there is NO added distance if word1[i] == word2[j]
    - If the two characters DO NOT match, we have three choices, each of which cost 1 edit: Insert, delete, Replace
        - This is a potentially unboundedly complex problem
        - However, we can narrow down the potential branching in our tree: For any operation type, the optimal decision is to insert, delete, or replace the character such that word1[i] is equal to word2[j] (in other words, we'd only ever insert or replace the character at i to match word2[j])
        - This narrows our decision tree to branch in only three directions at each step
        - After each step, we are left with a sub-problem! We are looking for the minDistance for two new, smaller strings
        - We have a clear base case: the minDistance to or from an empty string is the length of the non-empty string, i.e.:
            - minDistance(a, b), len(a) = 0, len(b) = 10 // 10
            - minDistance(a, b), len(a) = 10, len(b) = 0 // 10
            - minDistance(a, b), len(a) = 0, len(b) = 0 // 0
    - Example case: word1 = "ab", word2 = "bc"
        - Compare "a" and "b", they do not match, so we know we have edit distance of at least 1, but which option should we choose?
            - Option 1 (INSERT): insert "b" before "a" -- this makes no sense, and we won't trace this further (more discussion on "insert" below)
            - Option 2 (DELETE): delete "a", resulting in "b" and "bc"
                - Tracing further, we'd find "b" == "b" (no edit distance), and "" has an edit distance of 1 from "c", resulting in a total of 1 additional edit on this path
            - Option 3 (REPLACE): replace "a" with "b", resulting in "bb" and "bc"
                - Tracing futher, we'd find "b" == "b" (no edit distance), and "b" does not equal "c", we can trace this path further, but we find an additional 1 edit on this path
        - Take the minimum distance (1) and add it to the edit we just had to make, resulting in a total distance of 2
    - Because we have a decision tree, and trees are naturally recursive, we can solve this using recursion
    - We can define our recursive function minimum_distance(word1: str, word2: str) -> int where at each step we return:
        - minimum_distance(word1[1:], word2[1:]), if word1[1] == word2[1]
        - OR min(delete(), replace(), insert())
    - Notice that here we need to copy a string on each step because we are INSERTING into a string, so we can't just use indices to the original string
    - However, we can observe that INSERTING word2[j] is the same as DELETING word2[j] from word2! That is, we never need to add any characters into any string,
      because we are ALWAYS adding in order to match, which we know adds no additional edit distance
    - In sum, we can define a recursive problem minimum_distance(idx1: int, idx2: int) -> int that recursively solves the minimum distance problem by repeatedly increasing
      one or both indices to shrink the problem down to sub-problems
    
    DP:
    - Immediately, we see that there are MANY ways to get to the same sub-problem fn(i, j)
    - By MEMOIZING these results, we can drastically reduce the complexity of the problem
    - Specifically, whereas before we had to make a maximum of max(m, n) (m = len(word1), n = len(word2)) iterations, each time branching 3 times (max(m, n)^3 complexity),
      we now need to only make 3(max(m, n)), or O(max(m, n)) computations -- we still need to visit all the possible combinations, but we don't need to solve them again once they
      are solved!
    - Our space complexity has contributions from the recursion stack (depth of max(m, n)) and the memo (size of max(m, n)), for a total of O(max(m, n))
    - Once we solve this recursively (more intuitive), we can take that code and transform it to an iterative solution for better performance and to avoid stack overflow with large inputs

    Optimization:
    - Now that we've solved this recursively, we can solve it iteratively. We'll keep the recursive code around as a reference and to build upon.
    - Whereas the recursive solution builds TOP DOWN with memoization, we will build BOTTOM UP with tabulation
    - Because we are building in the opposite direction, we must re-define our dp algorithm
    - Rather than solving for dp(i, j) where dp(i, j) represents the minimum distance for the slices STARTING with i, j, we can define dp[i][j] such that dp[i][j] represents the minimum distance to get TO the slices word1[:i], word2[:j]
    - In other words... dp[i][j] = {
        j, if i = 0 (the cost of deleting all j chars)
        i, if j = 0 (the cost of deleting all i chars)
        dp[i - 1][j - 1] if word1[i] == word2[j] (the cost of getting to i, j, and no more)
        min(
            dp[i - 1][j] # DELETION
            dp[i][j - 1] # INSERTION
            dp[i - 1][j - 1] # REPLACEMENT
        ) + 1
      }
    """


    def minDistance(self, word1: str, word2: str) -> int:
        # memo = dict()

        # def dp(idx1: int, idx2: int, memo: dict) -> int:
        #     if (idx1, idx2) in memo:
        #         return memo[(idx1, idx2)]

        #     if idx1 > len(word1) - 1: # if we've exhausted word1, the edit distance is however many characters are left in word2
        #         return len(word2) - idx2 # e.g., word2 = "abc", idx2 = 1, edit distance should be 2 (DELETE "bc")
            
        #     if idx2 > len(word2) - 1:
        #         return len(word1) - idx1
            
        #     if word1[idx1] == word2[idx2]: # optimal case, there's no edit distance whatsoever at these characters
        #         # shrink the sub-problem, and add nothing to it!
        #         result = dp(idx1 + 1, idx2 + 1, memo)
        #     else: # the two words don't match, either INSERT, DELETE, or REPLACE
        #         # INSERT to word1 is just DELETE from word2, so shrink word2...
        #         insert = dp(idx1, idx2 + 1, memo)
        #         # DELETE trivially deletes whatever the character is in word1 that we don't like...
        #         delete = dp(idx1 + 1, idx2, memo)
        #         # REPLACE will always replace word1[idx1] to equal word2[idx2], so delete idx1 and idx2 from the search space!
        #         replace = dp(idx1 + 1, idx2 + 1, memo)
        #         result = min(insert, delete, replace) + 1 # don't forget to add 1 for the extra operation we took to *get* here
            
        #     memo[(idx1, idx2)] = result
        #     return result

        
        # return dp(0, 0, memo)

        m, n = len(word1), len(word2)
        dp = [[0] * (n + 1) for _ in range(m + 1)] # create M + 1 x N + 1 DP matrix (+1 to support 0 as the empty string)
        
        for i in range(m + 1): # for each row, the first value's min distance is however many chars are left in word1
            dp[i][0] = i

        for j in range(n + 1): # for each column, the first value's mind distance is however many chars are left in word2
            dp[0][j] = j
        
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if word1[i - 1] == word2[j - 1]: # chars match, no added edit distance to reach i, j!
                    dp[i][j] = dp[i - 1][j - 1]
                else:
                    insert = dp[i][j - 1]
                    delete = dp[i - 1][j]
                    replace = dp[i - 1][j - 1]
                    dp[i][j] = min(insert, delete, replace) + 1
        
        return dp[m][n]



import pytest

@pytest.mark.parametrize(
    "word1,word2,expected",
    [
        ("horse", "ros", 3),
        ("intention", "execution", 5),
        ("dog", "", 3),
        ("", "fruit", 5),
        ("", "", 0),
    ]
)
def test_min_distance(word1, word2, expected):
    s = Solution()
    a = s.minDistance(word1, word2)
    assert a == expected

if __name__ == "__main__":
    pytest.main(['-v'])