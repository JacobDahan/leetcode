class Solution:

    # 1 <= nums.length <= 5000
    # -104 <= nums[i] <= 104
    # All values of nums are unique.
    # nums is an ascending array that is possibly rotated.
    def search(self, nums: List[int], target: int) -> int:
        # What we know:
        # - nums is an ascending array of unique elements
        # - nums may be rotated at some unknown axis
        #   For example, [0,1,2,4,5,6,7] might be left rotated by 3 indices and become [4,5,6,7,0,1,2]
        # - If this was simply an ascending array, we could use binary search
        # - Since this is rotated, we have to use a modified binary search

        # We can do this in two steps:
        # 1. Find the pivot point
        # 2. Binary search with an adjustment for the pivot

        # First, find the pivot
        # The pivot is defined as the smallest element in the array, or, more explicitly,
        # the smallest element such that elem <= nums[len(nums) - 1]
        left, right = 0, len(nums) - 1
        pivot = right
        while left <= right:
            mid = left + ((right - left) // 2)
            val = nums[mid]

            # If val is greater than the last number in the array, we must "look right", as we are "pre-pivot"
            if val > nums[-1]:
                left = mid + 1
            # If val is less than the last number in the array, we may have our pivot point,
            # but search for a better answer
            elif val < nums[-1]:
                pivot = mid
                right = mid - 1
            else:
                pivot = mid
                break
        
        # Optimally, we can do this in a single binary search with a shift accounting for the pivot

        # To start, just run two binary searches along [0, pivot - 1] and [pivot, n - 1]
        left, right = 0, pivot - 1
        while left <= right:
            mid = left + ((right - left) // 2)
            val = nums[mid]
            if val > target:
                right = mid - 1
            elif val < target:
                left = mid + 1
            else:
                return mid
        
        # If we didn't find anything, the value must be in [pivot, n - 1] (or nowhere at all!)
        left, right = pivot, len(nums) - 1
        while left <= right:
            mid = left + ((right - left) // 2)
            val = nums[mid]
            if val > target:
                right = mid - 1
            elif val < target:
                left = mid + 1
            else:
                return mid
            
        return -1