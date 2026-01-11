class Solution:
    """
    There is an integer array nums sorted in non-decreasing order (not necessarily with distinct values).

    Before being passed to your function, nums is rotated at an unknown pivot index k (0 <= k < nums.length)
    such that the resulting array is [nums[k], nums[k+1], ..., nums[n-1], nums[0], nums[1], ..., nums[k-1]] (0-indexed). 
    
    For example, [0,1,2,4,4,4,5,6,6,7] might be rotated at pivot index 5 and become [4,5,6,6,7,0,1,2,4,4].

    Given the array nums after the rotation and an integer target, return true if target is in nums, or false if it is not in nums.

    You must decrease the overall operation steps as much as possible.
    """

    def search(self, nums: List[int], target: int) -> bool:
        """
        Approach:
        - We are asked to SEARCH for a target element in a (partially) ordered array
        - This indicates that we may want to use BINARY SEARCH, which lets us reduce the search space in half
          at each step (giving us O(log n) runtime complexity, O(1) space complexity)
        - But binary search is typically used on SORTED arrays, how can we apply here?

        Observations:
        - For any array rotated at any index k (0 <= k < nums.length), we can take any index i and find that there exists
          at least one fully-sorted array to the right or left of i
            - if i < k, all elements on [0, i] must be sorted
            - if i > k, all elements on [i, nums.length] must be sorted
            - if i == k, all elements on [0, i) and [i, nums.length] must be sorted
        - In standard binary search, we discard one half of the array because we can guarantee the answer does not fall in
          those bounds, and we do so because the search space is sorted
        - Here, half of our search space is sorted at any time, so we can deterministically say "does x fall in [a, b]"
        - The question then becomes: How do we determine if one side is sorted?
            - If there were no duplicates, it would be trivial (nums[a] < nums[b])
            - With duplicates, a side is "sorted" when nums[a] == nums[b] and all elements c (a < c < b) nums[c] == nums[a] == nums[b]
            - ... We can say that isLeftSorted(b) := nums[b] > nums[a] or (nums[b] > nums[b - 1] and isLeftSorted(b - 1))
        
        Binary Search:
        - We are executing the simplest form of binary search: Range elimination
        - For this form of binary search, we have a trivial invariant: if target exists in nums, it must lie within [lo, hi] (inclusive)
        - At each step, we narrow our search space in half by making assertions against the SORTED side of the array
        - If lo and hi cross over, we did not find an answer
        - If we find an answer, we can return early (as we don't need the first or last, just ANY)
        """

        lo, hi = 0, len(nums) - 1 # to start, the entire search range is valid along [lo, hi]
        while lo <= hi: # we search with the invariant that IF target exists in nums it must exist along [lo, hi]
                        # so we need to check when lo == hi (we have no guarantee it is an answer)
            
            midpoint = lo + (hi - lo) // 2 # there is no int overflow in Python, still we practice good habits
            mid_val = nums[midpoint]

            if mid_val == target:
                return True # target found, no need to continue
            
            if nums[lo] == mid_val: # we can't reason about sorting here (e.g., [1, 0, 1, 1, 1])
                                    # however, we KNOW that target != mid_val, so we can drop lo from our answer space
                                    
                lo += 1 # in a pathological case (e.g., [1, 1, 1, 1, 1]), we will simply iterate the entire array (O(n) runtime)
                continue

            if nums[lo] < mid_val: # LHS is sorted, we can assertively say if target may fall in that sub-array
                if target >= nums[lo] and target < mid_val: # if target exists, will fall between [lo, midpoint - 1]
                    hi = midpoint - 1
                else: # target must not exist beetween [lo, midpoint]
                    lo = midpoint + 1
            else: # LHS is not sorted, which means RHS definitionally is
                if target > mid_val and target <= nums[hi]: # if target exists, will fall between [midpoint + 1, hi]
                    lo = midpoint + 1
                else: # target must not exist between [midpoint, hi]
                    hi = midpoint - 1

        return False # we only reach this line when the search space has been exausted and target not in nums
