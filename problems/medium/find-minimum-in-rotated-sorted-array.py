class Solution:
    """
    Suppose an array of length n sorted in ascending order is rotated between 1 and n times. 
    For example, the array nums = [0,1,2,4,5,6,7] might become:

        [4,5,6,7,0,1,2] if it was rotated 4 times.
        [0,1,2,4,5,6,7] if it was rotated 7 times.

    Notice that rotating an array [a[0], a[1], a[2], ..., a[n-1]] 1 time results in the array [a[n-1], a[0], a[1], a[2], ..., a[n-2]].

    Given the sorted rotated array nums of unique elements, return the minimum element of this array.

    You must write an algorithm that runs in O(log n) time.
    """
        
    def findMin(self, nums: List[int]) -> int:
        """
        Observations:
        - We are asked to SEARCH for the index of an element in an ordered array
        - The array was once sorted before being rotated between 1 and n times
        - When an array is rotated k times, it maintains the following property:
            - For all elements [0, ..., n-1-k], the array remains sorted
            - For all elements [n-k, ..., 0), the array remains sorted
            - In other words: There are two sorted sub-arrays that comprise the greater array
        - The minimum of the array is the original first element of the array, which is the first
          element for which nums[-1] > nums[i]

        Approach:
        - We are asked to SEARCH for an element meeting some predicate in an ordered array,
          this suggests that we should use binary search (and, specifically, the boundary convergence
          form of binary search)
            - In boundary convergence, we look for either the first or last element to meet a given predicate
            - Here, we want the FIRST element satisfying the predicate nums[i] < nums[-1]
            - Therefore, we follow the general MINIMIZATION structure for binary search
            - Our invariant is: We keep a search bounds [lo, hi], where all values i >= hi satisfy the condition,
              and all values i < lo do not (lo and all values in the search bounds are not yet checked)
        - How can we use binary search in a non-sorted array?
            - If we are searching for an element at index i, we are guaranteed that either
              all elements j, j > i are sorted (j in our search domain), or j < i, or both
        - Binary search runs in O(log n) time because it enables us to cut down the search space by half
          at each step (and O(1) space)
        """
        if not nums:
            return -1

        lo, hi = 0, len(nums) - 1
        while lo < hi: # when lo == hi, we know (by our invariant definition) that we found the first element
                       # that satisfies the predicate (nums[mid] < nums[hi])
            midpoint = lo + (hi - lo) // 2 # No int overflow in Python, but good habits...

            if nums[midpoint] < nums[hi]:
                # this is a valid answer, but perhaps not the first value to satisfy the predicate
                # per our invariant, all i >= hi must satisfy the predicate, so move hi
                hi = midpoint
            else:
                # midpoint does not satisfy the predicate
                # our invariant dictates that all values i that do not satisfy the predicate must be i < lo, so move lo
                # and discard this value
                lo = midpoint + 1

        return nums[lo]