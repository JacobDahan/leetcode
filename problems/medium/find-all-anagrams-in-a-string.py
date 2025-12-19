# Given two strings s and p, return an array of all the start indices of p's anagrams in s.
# You may return the answer in any order.

class Solution:
    def findAnagrams(self, s: str, p: str) -> List[int]:
        # Sliding window (O(n)):
        # - We can iterate through `s` one character at a time (i)
        # - For each character c, track the counter of c's occurrences
        # - If i >= len(p), for each character, add c to the counter and remove the c at i - len(p)
        len_s, len_p = len(s), len(p)
        if len_s < len_p:
            # no anagrams!
            return []
        
        s_count, p_count = [0] * 26, [0] * 26

        # Fill p up!
        for c in p:
            p_count[ord(c) - ord('a')] += 1
        
        i = 0
        anagrams = []

        while i < len_s:
            c = s[i]
            # Add the new letter to our counter
            s_count[ord(c) - ord('a')] += 1
            # Remove the old letter, IFF i >= len(p) (e.g., i = 3 and we are looking for a 3 character string)
            if i >= len_p:
                c_old = s[i - len_p]
                s_count[ord(c_old) - ord('a')] -= 1
            # Check if the counts match
            if s_count == p_count:
                anagrams.append(i - len_p + 1)
            
            i += 1

        return anagrams