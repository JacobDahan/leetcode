# Given an array of integers nums sorted in non-decreasing order, 
# find the starting and ending position of a given target value.
# 
# If target is not found in the array, return [-1, -1].
# 
# You must write an algorithm with O(log n) runtime complexity.


class Solution:
    def searchRange(self, nums: List[int], target: int) -> List[int]:
        # Observations:
        # - The list nums is non-decreasing (e.g., [1, 2, 2, 3, 3, 3, 4])
        # - For any given index i, we can perform a binary search to determine if it is the FIRST instance of target
        # - ... And same for LAST

        if not nums:
            return [-1, -1]

        left, right = 0, len(nums) - 1
        while left < right:
            mid = left + ((right - left) // 2)
            val = nums[mid]
            if target > val:
                left = mid + 1
            else:
                # Keep the mid element, in case it is the first instance of our value
                right = mid

        first_idx = left if nums[left] == target else -1
        
        # We only need to search from the first index onwards...
        left, right = first_idx, len(nums) - 1
        while left < right:
            mid = left + ((right - left) // 2)
            val = nums[mid]
            if target > val:
                left = mid + 1
            elif target < val:
                right = mid - 1
            else: # val == target
                if mid + 1 < len(nums) and nums[mid + 1] == target: # another answer exists
                    left = mid + 1
                else: # this is the last occurrence
                    left = mid
                    break

        last_idx = left if nums[left] == target else -1

        return [first_idx, last_idx]