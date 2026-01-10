class Solution:
    def search(self, nums: List[int], target: int) -> int:
        """
        Given an array of integers nums which is sorted in ascending order, and an integer target, 
        write a function to search target in nums. 
        
        If target exists, then return its index. Otherwise, return -1.

        You must write an algorithm with O(log n) runtime complexity.
        """
        # We are given an array in SORTED, ASCENDING order
        # We are asked to find the index of an integer target in the array
        # Whenever we see sorted arrays and a SEARCH, we should think BINARY SEARCH
        # We are also instructed to execute this search in O(log n) time...
        # Binary search works by reducing the search space in half at each step, resulting in O(log n)

        # How do we search for an element?
        # We define a search space [lo, hi] and declare the invariant that:
        # IF TARGET EXISTS IN NUMS, TARGET MUST FALL ALONG [lo, hi]
        # At each step, we can check the midpoint between lo and hi; if it equals our target, return...
        # ... otherwise, DISCARD the midpoint and continue searching (our invariant requires this!)
        # When lo and hi "cross over" (lo > hi), we can say that no elements match our target and return -1
        lo, hi = 0, len(nums) - 1
        while lo <= hi: # we have to check when lo == hi because lo and hi are both candidates in the search space
            mid = lo + ((hi - lo) // 2)
            val = nums[mid]
            
            if val == target:
                return mid
            
            # if target exists, it must exist to the LEFT of val
            if val > target:
                hi = mid - 1 # discard mid, it's not a valid answer
            # if target exists, it must exist to the RIGHT of val
            else:
                lo = mid + 1
        
        # lo > hi, meaning we can search no further and the element does not exist
        return -1