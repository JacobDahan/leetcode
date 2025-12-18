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
        # - At any given index i, if target > nums[i], the number must be to the right (or not present)
        # - At any given index j, if target < nums[j], the number must be to the left (or not present)
        # - At any given index k, if target == nums[k]:
        #   TODO: Improve this algo...
        #   - if nums[L] != k, L += 1
        #   - elif nums[R] != k, R -= 1
        #   - else: return [L, R]
        if not nums:
            return [-1, -1]

        left, right = 0, len(nums) - 1
        while left < right:
            mid = left + ((right - left) // 2)
            val = nums[mid]
            if target > val:
                left = mid + 1
            elif target < val:
                right = mid - 1
            else: # val == target
                if nums[left] != target:
                    left += 1
                elif nums[right] != target:
                    right -= 1
                else:
                    return [left, right]
        
        if nums[left] == target:
            return [left, left]
        else:
            return [-1, -1]
