from collections import Counter

class Solution:
    # Given two strings s1 and s2, return true if s2 contains a permutation of s1, or false otherwise.
    # In other words, return true if one of s1's permutations is the substring of s2.
    def checkInclusion(self, s1: str, s2: str) -> bool:
        # Naive / Brute Force:
        # - Iterate over s2 substrings of size len(s1)
        # - For each substring s_s2, sort the substring and compare to sorted(s1)
        # - If match, return True; else continue
        # - Complexity: [ l1 * log l1 ] (sort) * l2

        # Improved / Sliding Window:
        # - Iterate over s2 with a sliding window of size len(s1)
        # - For each window, count the occurrences of each car and compare to count_s1
        # - If match, return True; else continue
        # - Complexity: [ l2 * l1 (count) ]

        # Optimal / Improved Sliding Window:
        # - Iterate over s2 with a sliding window of size len(s1)
        # - For each window, update the occurrences of each char by removing the char that just fell
        #   out of the window, and adding the value that just came into the window
        # - If match, return True; else continue
        # - Complexity: [ l2 ]

        # Further Optimized:
        # - Same as above, but use array in place of counter
        len_s1, len_s2 = len(s1), len(s2)
        if len_s2 < len_s1:
            return False
        
        count_s1, count_s2 = [0] * 26, [0] * 26

        for c in s1:
            count_s1[ord(c) - ord('a')] += 1
        
        # Iterate over S2
        for i in range(0, len_s2):
            c = s2[i]

            count_s2[ord(c) - ord('a')] += 1

            if i >= len_s1:
                old_c = s2[i - len_s1]
                count_s2[ord(old_c) - ord('a')] -= 1
            
            if count_s1 == count_s2:
                return True
        
        return False