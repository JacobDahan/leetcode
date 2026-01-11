class Solution:
    """
    A peak element is an element that is strictly greater than its neighbors.

    Given a 0-indexed integer array nums, find a peak element, and return its index. 
    If the array contains multiple peaks, return the index to any of the peaks.

    You may imagine that nums[-1] = nums[n] = -∞. In other words, an element is always considered to 
    be strictly greater than a neighbor that is outside the array.

    You must write an algorithm that runs in O(log n) time.
    """

    def findPeakElement(self, nums: List[int]) -> int:
        """
        Observations:
        - We are asked to SEARCH for an element that matches a predicate in an array
        - We are asked to execute this search in O(log n) time
        - These criteria indicate that we should consider binary search

        ... But the array is not sorted! How can we execute binary search?
        - We need to carefully define our invariants:
            - A peak is an element i such that nums[i - 1] < nums[i] < nums[i + 1]
            - An element is considered strictly greater than a neighbor that is outside the array
            - We are told nums[i] != nums[i + 1] for all valid i
        - For any given element, then, its neighbors must be greater than or lesser than it:
            - if both neighbors are less than it, it is the peak, return
            - if the left neighbor is greater than it, there must exist a leftward peak
                - Either the left neighbor is peak
                - ... Or there exists a peak left of it
                - ... Or it is monotonically increasing towards the boundary, and the boundary is the peak!
            - if the right neighbor is greater than it, there must exist a rightward peak
        - So our invariant becomes: We guarantee that a peak exists along [lo, hi]
        """
        def is_peak(i):
            """
            Returns True if the element at nums[i] is a peak, else False.
            """
            gt_left = i == 0 or nums[i] > nums[i - 1]
            gt_right = i == len(nums) - 1 or nums[i] > nums[i + 1]
            return gt_left and gt_right

        lo, hi = 0, len(nums) - 1 
        while lo <= hi: # our invariant specifies that a peak exists within this range,
                        # but still have to check for the peak at each step, and the peak may exist at lo == hi
            
            midpoint = lo + (hi - lo) // 2 # Python doesn't risk int overflow, but practice!!
            
            if is_peak(midpoint):
                return midpoint
            
            if midpoint > 0 and nums[midpoint] < nums[midpoint - 1]: # there must exist a peak to the left
                hi = midpoint - 1
            else: # there must exist a peak to the right
                lo = midpoint + 1
        
        # unreachable, but let's code defensively...
        return -1