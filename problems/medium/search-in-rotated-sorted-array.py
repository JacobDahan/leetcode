class Solution:
    """
    There is an integer array nums sorted in ascending order (with distinct values).

    Prior to being passed to your function, nums is possibly left rotated at an unknown index k 
    (1 <= k < nums.length) such that the resulting array is [nums[k], nums[k+1], ..., nums[n-1], 
    nums[0], nums[1], ..., nums[k-1]] (0-indexed). 
    
    For example, [0,1,2,4,5,6,7] might be left rotated by 3 indices and become [4,5,6,7,0,1,2].

    Given the array nums after the possible rotation and an integer target, 
    return the index of target if it is in nums, or -1 if it is not in nums.

    You must write an algorithm with O(log n) runtime complexity.
    """

    def search(self, nums: List[int], target: int) -> int:
        """
        - We are being asked to SEARCH in an ORDERED array (ascending, no distinct values)
        - Whenever we see these terms, we should think BINARY SEARCH (an O(log n) runtime / O(1) space complexity algo
          for searching ordered arrays)
        - ... But this is not a *sorted* array, because it has been rotated at some unknown index k
        - So, how can we execute a binary search?

        Option 1: Two binary searches
        - In a first binary search, we can use the "boundary convergence" form binary search to find the rotation index
            - In boundary convergence, we need a predicate and an invariant
            - We can call our predicate "isRotationAxis" and look for the FIRST index that satisfies the predicate
              (note this is the traditional "minimization" algo)
            - Then, we just need to define our invariant: All indices i, i < lo must not satisfy the predicate;
              all indices i, i >= hi must satisfy the predicate
            - Therefore, we search until lo == hi, at which point lo is guaranteed to satisfy the predicate
        - In a second binary search, we simply search the "correct slice" of the array
            - if target > nums[0], search lo = 0, hi = axis - 1
            - if target < nums[0], search lo = axis, hi = len(nums) - 1
            - We can use "normal" binary search because the portion of the array we are searching is guaranteed to be non-rotated

        Option 2: One binary search
        - What do we know about an array possibly sorted at index k?
            - For any index i, the at least one sub-array [lo, i] or [i, hi] must be sorted
            - With a single given sub-array, we can trivially determine whether the answer MAY NOT exist in that sub-array
            - In other words, we can ensure the following invariant is true without looking at the unsorted slice:
                FOR THE SUB-ARRAY [lo, hi], THE TARGET MUST EXIST WITHIN THE BOUNDS IF IT EXISTS IN THE ARRAY nums
        - Specifically, how do we do this?
            - First, check if the midpoint is equal to our target and return
            - Next, determine if the left sub-array is sorted (if nums[mid] >= nums[lo])
                - If target does not fall in bound [nums[lo], nums[mid]], discard (else keep)
            - Else, the right sub-array must be sorted (nums[mid] < nums[hi])
                - If target does not fall in bound [nums[mid], nums[hi]], discard (else keep)
        """
        # Option 1
        # return self.findAxisAndSearch(nums, target)
        # Option 2
        return self.searchRotatedArray(nums, target)

    def findAxisAndSearch(self, nums: List[int], target: int) -> int:
        if not nums:
            return -1
        
        # First, look for the rotation axis
        lo, hi = 0, len(nums) # to ensure our predicate is true, hi must not point to an element to start 
                              # (this makes the i >= hi satisfies statement vacuous, but true!)
                              # we just need to verify that lo != len(nums) later on for an array with no rotation
        
        def isRotationAxis(i):
            # simply, if nums[i] < nums[0], this must be at or beyond the rotation axis
            return nums[i] < nums[0]

        while lo < hi: # when the two converge, we have found our answer, by definition of the invariant
            midpoint = lo + (hi - lo) // 2 # Python doesn't have int overflow, but good practice

            if isRotationAxis(midpoint):
                # this is at or beyond the rotation axis, but it may not be the FIRST element beyond the rotation axis
                # keep this as a "valid" answer, but look "leftwards"
                hi = midpoint
            else:
                # this is not a valid answer
                # our invariant is clear: any values that don't satisfy the predicate must sit BELOW lo
                # discard this value and look right
                lo = midpoint + 1
        
        # if lo == len(nums), this is a non-rotated array - just search
        if lo == len(nums):
            lo, hi = 0, len(nums) - 1
        # otherwise, search the appropriate slice of the array for the target...
        # we know that all values i < k are greater than nums[k] and nums[n] (n > k, n < len(nums))
        # therefore, by simply checking the target in relation to i = 0, we can determine our slice!

        # target is greater than an element greater than all elements beyond axis, look left of axis
        elif target >= nums[0]:
            lo, hi = 0, lo
        
        # target is less than the smallest rotated element, look right of axis
        else:
            lo, hi = lo, len(nums) - 1

        while lo <= hi: # new invariant: if target exists, it must lie between [lo, hi]
                        # so we must check when lo == hi, as this may or may not contain the target
            midpoint = lo + (hi - lo) // 2
            mid_val = nums[midpoint]

            if mid_val == target:
                return midpoint 
            
            if mid_val > target:
                # midpoint is too far right in this slice, look leftwards for target and discard midpoint
                hi = midpoint - 1
            else:
                lo = midpoint + 1
        
        return - 1

    def searchRotatedArray(self, nums: List[int], target: int) -> int:
        if not nums:
            return -1
        
        lo, hi = 0, len(nums) - 1

        # Invariant: If target exists in nums, it must exist between [lo, hi] (inclusive)

        while lo <= hi: # because of our invariant, we must check when lo == hi
                        # the mere fact that lo == hi does not guarantee that we have a valid answer
            
            midpoint = lo + (hi - lo) // 2 # Python doesn't have int overflow, but good practice
            mid_val = nums[midpoint]

            if mid_val == target:
                return midpoint
            
            if mid_val >= nums[lo]: # left sub-array is sorted (use >= in case midpoint == lo, we need to be able to progress)
                if target < mid_val and target >= nums[lo]:
                    # the target must exist between lo (inclusive) and midpoint (exclusive) if it exists in nums, so adjust our search space
                    hi = midpoint - 1
                else:
                    # the target MAY NOT exist between lo and midpoint (inclusive), so discard the entire sorted sub-array
                    lo = midpoint + 1
            else: # right sub-array is sorted
                if target > mid_val and target <= nums[hi]:
                    # the target must exist between midpoint (exclusive) and hi (inclusive) if it exists in nums, so adjust our search space
                    lo = midpoint + 1
                else:
                    # the target MAY NOT exist between midpoint and hi (inclusive), so discard the entire sorted sub-array
                    hi = midpoint - 1
        
        # no match, return -1
        return -1