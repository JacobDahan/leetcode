class Solution:
    # Given a 0-indexed integer array nums, find a peak element, and return its index. 
    # If the array contains multiple peaks, return the index to any of the peaks.
    def findPeakElement(self, nums: List[int]) -> int:
        # How can we do this in O(log n)?
        # - We need to cut the list down in half each time
        # - Because the list has no sorting, we have no way of saying definitively that one half
        #   cannot hold the answer
        # - However, we CAN say that one half DOES hold the answer:
        #   - For any given idx i such that nums[i] < nums[i+1], a peak must exist to the right. Why?
        #       - The elements to the right may be monotonically increasing (j > i, nums[j] > nums[i]), such that
        #         at the very least the last element nums[j] (j == len(n) - 1) is a peak, since
        #         nums[j] > nums[j - 1] and nums[j] > -inf
        #       - Else, the elements to the right may at some point decrease (j > i, nums[j] < nums[i]),
        #         guaranteeing that a peak exists, since nums[i] < nums[j] < nums[k] (k > j > i)
        #   - For any given idx i such that nums[i] < nums[i-1], a peak must exist to the left, for the opposite reason

        left, right = 0, len(nums) - 1
        while left < right:
            mid = left + ((right - left) // 2)
            peak = nums[mid]
            gt_right = True if mid + 1 >= len(nums) else (peak > nums[mid + 1])

            if not gt_right:
                # Right is greater, we are guaranteed to have a peak to the right
                left = mid + 1
            else:
                # This may be peak, or peak may be to the left
                right = mid
        
        return left
        