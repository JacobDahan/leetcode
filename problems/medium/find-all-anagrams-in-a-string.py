# Given two strings s and p, return an array of all the start indices of p's anagrams in s.
# You may return the answer in any order.
from collections import Counter

class Solution:
    def findAnagrams(self, s: str, p: str) -> List[int]:
        # Intuition:
        # - For any problem where we need to find indices that match a pattern,
        #   we can use a sliding window approach
        # - This gives us a LINEAR solution O(n) in complexity
        # - How do we use a sliding window?
        #   - We can keep track of exactly what we have seen at each step
        #   - Either use a counter dict, or use an array (since the possibilities
        #     are tightly bound to 26 lower case characters)
        #   - Dicts are expensive and make comparison less trivial, it's much easier for a small
        #     set to use an array
        len_s, len_p = len(s), len(p)
        if len(s) < len(p):
            # no possible solutions
            return []
        
        s_counts, p_counts = [0] * 26, [0] * 26

        # Update p counts
        for c in p:
            p_counts[ord(c) - ord('a')] += 1
        
        # Now, iterate through s and update that counts for each char
        answers = []
        for idx in range(0, len_s):
            window_start = idx - len_p + 1
            char = s[idx]

            # Add one for the char that just came into the window
            s_counts[ord(char) - ord('a')] += 1

            # If we have seen (len_p + 1) elements already, we have too many elements in our counter!
            # We need to remove whatever has fallen out of our sliding window
            if window_start > 0:
                old_char = s[window_start - 1]
                s_counts[ord(old_char) - ord('a')] -= 1
            
            if s_counts == p_counts:
                answers.append(window_start)
        
        return answers


    # def findWithDict(self, s: str, p: str) -> List[int]:
    #     len_s, len_p = len(s), len(p)
    #     if len(s) < len(p):
    #         # no possible solutions
    #         return []

    #     # Using a counter dict
    #     s_counter, p_counter = Counter(), Counter(p)

    #     # For each char in s, update the counter, and check for equality
    #     answers = []
    #     for idx in range(0, len_s):
    #         char = s[idx]
            
    #         # Update the counter to reflect the char at idx
    #         s_counter[char] += 1

    #         # If we have seen (len_p + 1) elements already, we have too many elements in our counter!
    #         # We need to remove whatever has fallen out of our sliding window
    #         if idx >= len_p:
    #             old_char = s[idx - len_p] # e.g., idx = 3, p = 3, only keep elements at idxs [1, 2, 3]
    #             if s_counter[old_char] == 1:
    #                 del s_counter[old_char]
    #             else:
    #                 s_counter[old_char] -= 1
            
    #         # Now, check if the two counters are identical
    #         if s_counter == p_counter:
    #             # That's a match!
    #             answers.append(idx - len_p + 1)
        
    #     return answers