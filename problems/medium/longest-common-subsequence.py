"""
Given two strings text1 and text2, return the length of their longest common subsequence. If there is no common subsequence, return 0.

A subsequence of a string is a new string generated from the original string with some characters (can be none) deleted without changing the relative order of the remaining characters.

    For example, "ace" is a subsequence of "abcde".

A common subsequence of two strings is a subsequence that is common to both strings.
"""

class Solution:
    """
    Task:
    - We are asked to find the longest common subsequence (LCS) between two strings (text1 and text2)
    - An LCS is a common subsequence between two strings
    - A subsequence is any sequence of characters that appear in order in the original string, with zero or more interleaved characters from the original deleted

    Observations:
    - We are being asked to OPTIMIZE (MAXIMIZE) a solution, which suggests that we should consider greedy or DP algorithms
    - A greedy algorithm is provably incorrect: e.g., for "adbc" and "abcd", the optimal solution is 3 ("abc"), NOT 2 ("ad")
    - Therefore, we should consider DP
    - Before we jump into DP, let us consider how we might solve the problem by brute force, as this will help us understand the recurrence relationship (if one exists)

    Brute force:
    - Let's think about how we would solve this by hand...
    - We're going to need to go character by character in both text1 and text2, since we're going to have to make a decision in each string about whether to include it in the LCS
    - So we can walk through a simple example: text1 = "adbc" and text2 = "abcd"
        - Step 1: the first character of both strings is "a" -- we should definitely include this, since there's no way that we can find a LONGER substring than taking the first element!
        - Step 2: since we "used up" the first character, now we're comparing "d" and "b" -- I have no way of knowing what to include, so I think we'll have to try both
            - Step 3a: I'll keep "d" and get rid of the "b" from text2, since I need to make some progress... Now I'm comparing "b" and "c"... Again, no match...
                - Step 4a: I'll keep "d" and get rid of "c" from text 2... Ah! Now I've found another "d"! So I can increase my LCS to "ad"
                - Step 5a: Now I can progress to "b" and... Oh, there's nothing to compare it to... we've consumed the other string, so "ad" is my answer!
            - Step 3b: I'll discard "d" and keep "b" from text2... Now I'm, comparing "b" and "b"... A match! So "ab" is my best string
            - Step 4b: Now I'm comparing "c" and "c"... Another match! "abc" is now my best string
            - Step 5b: Now I'm comparing... wait... I have nothing left in text1, so I guess I'm done! "abc" is my answer, and it's longer than "ad", so that's the best I can done
    - We can see a recursive structure here, where for each step, I'm shrinking one or both sub-arrays and trying to solve a smaller sub-problem
    - The sub-problem has base case where we run out of letters (LCS = 0)
    - We can define our function simply as lcs(i, j) = {
        0, if i >= len(text1) or j >= len(text2)
        lcs(i + 1, j + 1) + 1, if text1[i] == text2[j]
        max(lcs(i + 1, j), lcs(i, j + 1)), otherwise
      }
    - What we notice is that there are multiple possible paths to reach any lcs(i, j), so we want to MEMOIZE it
    - This is what transforms our brute force solution into DP
    - Once we have a good undestanding of the recurrence relationship and working code, we can perhaps optimize to an iterative solution that will execute without the overhead of recursion AND avoid stack overflow risk for large inputs

    DP:
    - Recurrence relationship: dp(i, j) = {
        dp(i + 1, j + 1) + 1, if text1[i] == text2[j]
        max(dp(i + 1, j), dp(i, j + 1)), otherwise
      }
    - Base case: dp(i, j) = 0 if i >= len(text1) or j >= len(text2)

    Complexity:
    - In the worst case, we will have to visit all possible solutions dp(i, j) exactly Once
    - This is maximally N * M solutions, where N = len(text1) and M = len(text2)
    - For this reason, runtime complexity is O(N * M)
    - Similarly, since we need to store the answer for each of these, space complexity is O(N * M)
    - We also have to consider the stack space used by our recursion stack, but this will never be deeper than N + M, and the multiplicative space complexity outweighs this

    Optimization:
    - For large values N or M, we will see stack overflow
    - Even without overflow, recursion has its own overhead that nontrivially impacts runtime
    - We can optimize our TOP-DOWN, MEMOIZED DP SOLUTION to a BOTTOM-UP, TABULATED SOLUTION
    - When we perform tabulation, we build up from smaller sub-problems to the bigger problem
    - This means we have to re-frame the recurrence relation:
        - dp(i, j) represented the LCS for the suffixes of text1, text2 starting at i, j, respectively
            - This allowed us to recursively dive DOWN to a base case, where dp(i, j) = 0
            - In the tabulated formulation, we have to build UP from a base case
        - dp[i][j] represents the LCS for the PREFIXES of text1, text2, up to and including i, j, respectively
            - In other words, dp[0][0] represents the LCS between "" and "", our base case again!
            - In fact, all dp[0][j] and dp[i][0] should be equal to zero!
    - Recurrence relationship: dp[i][j] = {
        dp[i - 1][j - 1] + 1, if text1[i] == text1[j] // think "a" and "a"; the answer would be the LCS of "" and "", plus one!
        max(dp[i - 1][j], dp[i][j - 1]), otherwise // think "ab" and "a"; the answer would be the maximum of the LCS of "a" and "a" (1) and "ab" and "" (0)!
      }
    - Base case: dp[i][j] = 0 for all i = 0 or j = 0
    """
    def longestCommonSubsequence(self, text1: str, text2: str) -> int:
        # def lcs(start1: int, start2: int, memo: dict) -> int:
        #     """
        #     Utility method to return the LCS for text1 and text2 sliced to start at start1 and start2, respectively.
        #     """
        #     if (start1, start2) in memo:
        #         return memo[(start1, start2)]
            
        #     if start1 >= len(text1) or start2 >= len(text2):
        #         return 0 # we've run out of characters! no more common ones can be found
            
        #     if text1[start1] == text2[start2]:
        #         # this is the BEST case: we can increase our LCS while making progress without skipping any letters
        #         result = lcs(start1 + 1, start2 + 1, memo) + 1 # make sure we add 1 to the LCS of the sub-problem, as we included this character in the LCS!
        #     else:
        #         # we cannot include this character in the LCS, but we have to make progress
        #         # do we skip the element in text1 or text2? we can't tell, so compute both and take the better
        #         result = max(lcs(start1 + 1, start2, memo), lcs(start1, start2 + 1, memo))
            
        #     memo[(start1, start2)] = result
        #     return result
        
        # return lcs(0, 0, dict())

        dp = [[0] * (len(text2) + 1) for _ in range(len(text1) + 1)] # create an array of N + 1 rows, M + 1 columns (+1 so that we can have a true "zero" column/row for empty strings)

        for r in range(1, len(text1) + 1): # iterate over rows
            for c in range(1, len(text2) + 1): # iterate over columns
                if text1[r - 1] == text2[c - 1]:
                    # the LCS we can form up to the prefixes text1[:i+1], text2[:j+1] is equal to the maximum we could form without this character, plus 1
                    dp[r][c] = dp[r - 1][c - 1] + 1
                else:
                    # the LCS we can form up to the prefixes is equal to the maximum we could form EITHER without the last character in text1 OR text2
                    dp[r][c] = max(dp[r - 1][c], dp[r][c - 1])
        
        return dp[len(text1)][len(text2)]

import pytest

@pytest.mark.parametrize(
    "text1,text2,expected",
    [
        ("abcde", "ace", 3),
        ("adbc", "abc", 3),
        ("abc", "abc", 3),
        ("abc", "def", 0),
        ("ezupkr", "ubmrapg", 2)
    ]
)
def test_lcs(text1, text2, expected):
    s = Solution()
    a = s.longestCommonSubsequence(text1, text2)
    assert a == expected, f"Expected {expected}, observed {a}"

if __name__ == "__main__":
    pytest.main(['-v', '-s'])