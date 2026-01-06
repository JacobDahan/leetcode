class Solution:
    def searchRange(self, nums: List[int], target: int) -> List[int]:
        """
        Given an array of integers nums sorted in non-decreasing order, 
        find the starting and ending position of a given target value.

        If target is not found in the array, return [-1, -1].

        You must write an algorithm with O(log n) runtime complexity.
        """
        # We are given that this is a non-drecreasing array (i.e., increasing, with duplicates).
        # Our goal is to find the start and end position of a given target value.
        # We are asked to do so with O(log n) runtime complexity.
        # Given that this sorted array search and we are told to use O(log n) runtime complexity, this suggests
        # binary search.

        # There are two forms of binary search:
        # Form 1: Closed interval search (invariant: if the answer exists in the array, it lies along [lo, hi])
        # Form 2: Boundary conversion (invariant: all values i < lo do not satisfy some condition, all i >= hi do
        #         -- or the opposite)
        # This question can be reframed as two separate binary searches:
        # 1. Find the last index i such that nums[i] < target (then add one)
        # 2. Find the first index i such that nums[i] > target (then subtract one)
        # These boundary searches lead naturally to the use of the boundary conversion form of binary search.
        
        # First task: find the last index i such that nums[i] < target
        def findLast():
            # This is a boundary search, meaning that we are not searching for a specific value,
            # but instead trying to converge a boundary while maintaining the invariant
            # Specifically, this is a "last-true" search with the invariant:
            # --> For all i <= lo, nums[i] < target; for all i > hi, nums[i] >= target
            # We search along the space (lo, hi], where any values greater than hi may never be valid
            lo, hi = -1, len(nums) - 1

            # When lo == hi, our search space has collapsed and we found our answer (if exists)
            while lo < hi:
                mid = lo + ((hi - lo + 1) // 2) # use ceiling division to avoid infinite loop
                val = nums[mid]

                if val >= target:
                    # This does not satisfy the condition, the invariant demands that we throw away
                    # this value and all values right of it
                    hi = mid - 1
                else:
                    # This satisfies the condition, but may not be optimal -- look rightward
                    lo = mid

            first_index = lo + 1 # last index i such that nums[i] < target, so add one for first index of target
            if first_index >= len(nums) or nums[first_index] != target:
                return -1
            
            return first_index
        
        # Second task: find the first index i such that nums[i] > target
        def findFirst():
            # This is a boundary search, meaning that we are not searching for a specific value,
            # but instead trying to converge a boundary while maintaining the invariant
            # Specifically, this is a "first-true" search with the invariant:
            # --> For all i < lo, nums[i] <= target; for all i >= hi, nums[i] > target
            # We search along the space [lo, hi), where any values less than lo may never be valid
            lo, hi = 0, len(nums)

            # When lo == hi, our search space along [lo, hi) has collapsed and we must be pointing at the value
            while lo < hi:
                mid = lo + ((hi - lo) // 2) # avoid int overflow; use floor division because we are converging
                                            # towards lo (use ceiling when converging towards hi)
                val = nums[mid]
                
                if val <= target:
                    # This does not meet the condition; this index and all leftward indices must be tossed
                    lo = mid + 1
                else:
                    # This meets the condition but may not be optimal, look leftward but keep the value
                    hi = mid
            
            # No fancy stuff here, we only call this if we know an element exists
            return hi - 1
        
        first = findLast()

        if first == -1:
            return [-1, -1]
        
        return [first, findFirst()]