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

            # Thank goodness, we found it!
            if val == target:
                return mid

            # We don't have a match, so we need to figure out what portion of the remaining problem space
            # is still in play. We can only make any assertions about the sorted bits of the problem space,
            # so check which side that is...

            # If the value is greater than the left-most item, we know the LHS is sorted
            if val >= nums[left]:
                # The target is greater than the value -- there is no possible answer on the LHS, so discard
                # Similarly, the target may be less than the smallest element on the LHS, so discard
                if val < target or target < nums[left]:
                    left = mid + 1
                else:
                    right = mid - 1
            # Otherwise, the RHS is sorted
            else:
                # The target is less than the value -- there is no possible answer on the RHS, so discard
                # Similarly, the target may be greater than the largest element on the RHS, so discard
                if val > target or target > nums[right]:
                    right = mid - 1
                else:
                    left = mid + 1
            
        return -1