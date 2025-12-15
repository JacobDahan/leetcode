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

        # We can do this in ONE binary search, we just have to be extremely cautious
        left, right = 0, len(nums) - 1
        while left <= right:
            mid = left + ((right - left) // 2)
            val = nums[mid]

            # If the value is greater than our target value...
            if val > target:
                # Ordinarily we'd look to the left, but here we don't have a guarantee that the list to the left
                # is still monotonically increasing

                # If the left-most number is smaller than our current number, we are guaranteed that the
                # LHS of the equation is sorted. If the target is smaller than those values, there is no answer
                # in that part of the array, so look to the right.
                if nums[left] <= val and target < nums[left]:
                    left = mid + 1
                # If the left hand side is not sorted, the right hand side must be sorted
                # and all values to the right are even greater than the current value, so there is no possible
                # answer in that portion of the array
                else:
                    right = mid - 1
            # If the value is less than our target value...
            elif val < target:
                if nums[right] >= val and target > nums[right]:
                    right = mid - 1
                else:
                    left = mid + 1
            else:
                return mid
            
        return -1