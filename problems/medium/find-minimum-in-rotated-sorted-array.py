class Solution:
    # Suppose an array of length n sorted in ascending order is rotated between 1 and n times.
    # Given the sorted rotated array nums of unique elements, return the minimum element of this array.
    def findMin(self, nums: List[int]) -> int:
        # brute force
        # min = float('inf')
        # for num in nums:
        #     if num < min:
        #         min = num
        # return min

        # What do we know?
        # - The array was once monotonically increasing
        # - There exists at most 1 "pivot" point that divides two monotonically increasing arrays
        
        # Option 1: We can find the pivot point using binary search, then search for the min trivially
        # Option 2: We can execute a modified binary search for the minimum
        
        # Option 2: How can we do this?
        # - No matter what point in the list we select, we have a sorted array on at least one side
        # - If the array is sorted on the right, it means that all the numbers to the right are greater than
        #   - So we must look left if nums[R] > nums[i]
        #   - i is still a valid answer!!!
        # - Else (if the array is not sorted on the right), it means by definition that a smaller number
        #   exists for some index j, i < j <= R

        left, right = 0, len(nums) - 1
        while left < right:
            mid = left + ((right - left) // 2)
            val = nums[mid]
            # Check if this value is less than the rightmost value
            # Recall, this used to be the greatest value
            # nums[right] can only be greater than nums[mid] if mid...right is still sorted,
            # meaning that mid is the smallest index on that interval
            if val < nums[right]:
                # mid is still a plausible answer!!!
                right = mid
            # If nums[mid] > nums[right], we know that nums[right] is either the minimum,
            # or that some minimum (the original index 0) exists between mid...right
            else:
                # we already know that nums[right] < nums[mid], so mid can never be the answer
                left = mid + 1
        
        return nums[left]