from typing import List

class Solution:
    """
    There is an integer array nums sorted in non-decreasing order (not necessarily with distinct values).

    Before being passed to your function, nums is rotated at an unknown pivot index k (0 <= k < nums.length) such that the resulting array is [nums[k], nums[k+1], ..., nums[n-1], nums[0], nums[1], ..., nums[k-1]] (0-indexed). For example, [0,1,2,4,4,4,5,6,6,7] might be rotated at pivot index 5 and become [4,5,6,6,7,0,1,2,4,4].

    Given the array nums after the rotation and an integer target, return true if target is in nums, or false if it is not in nums.

    You must decrease the overall operation steps as much as possible.
    """


    def search(self, nums: List[int], target: int) -> bool:
        """
        Task:
        - We are given an array nums that was sorted in non-decreasing order but may have duplicates
        - The array was rotated once at an index k (0 <= k < nums.length)
        - We are asked to find a target integer in the array nums and return true if it exists, otherwise false (NOT the index of the target)

        Observations:
        - When asked to find an integer in a sorted array, we typically reach for binary search, since this gives us O(log n) runtime
        - Binary search achieve the logarithmic runtime because we can trim the search space in half at every iteration
        - We can safely trim the search space because the array is sorted, which means that we can easily check if target X falls within the LHS or RHS
          of an array (split at index mid, our current search index)
        - Here, for any search index mid, we are guaranteed that one side of the array (one sub-array) is sorted
            - Why? We had a sorted array, and we only rotated it at one index
            - That index must either be to the left of our midpoint (LHS not sorted, RHS sorted) or to the right (RHS not sorted, LHS sorted), or is the midpoint
            - Therefore, we can make assertions about whether a target value may fall in the SORTED array, and discard or keep that side as our search space
        - One complication comes from the fact that this array has duplicates: Typically, we'd check if one side of the array is sorted by comparing our search midpoint
          to the element furthest left in our search space
            - Because of duplicates, this may be an equal value
            - In this case, we have NO WAY of knowing whether or not the array is sorted between lo and mid (could be [5, 1, 2, 5, 5, 5, 5] or [5, 5, 5, 0, 1, 2], for example)
            - BUT, we know that the target value is not equal to the mid value (else we would have returned), so we can simply discard this LHS value, too!
            - In the worst case -- an array of complete duplicates -- we end up having to iterate over every element in the array this way (O(n))
            - In the "standard" case (some duplicates), we approach optimal binary search O(log n) runtime complexity
        
        Algorithm:
        - Run a binary search with the invariant: IF target exists in nums, it must sit along [lo, hi]
        - Termination point: If the target is found, return True; if lo > hi, we have exhausted the search space, so return false
        - Search space: When lo == hi, we still must check the value, because the invariant does not guarantee that we found an answer
        - At each iteration, run the following logic:
            - If nums[mid] == nums[lo] == nums[hi], discard the lo AND hi values and continue (worst case O(n))
            - If nums[mid] == nums[lo], discard the lo value and continue (worst case O(n))
            - If nums[mid] > nums[lo], the LHS must be sorted, so keep if target in LHS, else discard LHS
            - If nums[mid] < nums[lo], the RHS must be sorted, so keep if target in RHS, else discard RHS
        """
        
        lo, hi = 0, len(nums) - 1 # the entire nums array is a valid search space to begin

        while lo <= hi: # why equals? when lo == hi, we only know that target may exist in the array at lo/hi, we have no guarantee that we found an answer -- so we have to check!
            mid = lo + (hi - lo) // 2 # Python can't int overflow, but take care regardless...
            mid_val = nums[mid]

            if mid_val == target:
                return True

            lo_val = nums[lo]
            hi_val = nums[hi]
            
            if mid_val == lo_val == hi_val: # no way to tell if EITHER side is sorted, but neither lo nor hi may be the answer, so discard
                lo += 1
                hi -= 1
            elif mid_val == lo_val: # no way to tell if the LHS is sorted or not, but lo MUST not be the answer, so discard
                lo += 1
            elif mid_val > lo_val: # LHS must be sorted (mid and lo are BOTH on one side of the rotation boundary)
                if target < mid_val and target >= lo_val:
                    # target MUST exist along [lo, mid - 1] IF exists in the array
                    hi = mid - 1
                else:
                    # target MUST NOT exist along [lo, mid - 1] IF exists in the array, so discard LHS
                    lo = mid + 1
            else: # LHS is not sorted, so RHS must be (mid and hi are BOTH on one side of the rotation boundary)
                if target > mid_val and target <= hi_val:
                    # target MUST exist along [mid + 1, hi] IF exists in the array
                    lo = mid + 1
                else:
                    # target MUST NOT exist along [mid + 1, hi] IF exists in the array, so discard RHS
                    hi = mid - 1
        
        # lo > hi, so we've exhausted the entire search space and target must not exist
        return False

# Test case: nums = [2,5,6,0,0,1,2], target = 0
# iter 1: lo = 0, hi = 6, mid = 3, val = 0 // return True

# Test case: nums = [2,2,2,2,0,1,2], target = 3
# iter 1: lo = 0, hi = 6, mid = 3, val = 2 // mid_val == lo_val == hi_val (increase lo, decrease hi)
# iter 2: lo = 1, hi = 5, mid = 3, val = 2 // mid_val == lo_val (search RHS); 3 > 2 (discard RHS)
# iter 3: lo = 1, hi = 2, mid = 1, val = 2 // mid_val == lo_val == hi_val (increase lo, decrease hi)
# iter 4: lo > hi // return False

import pytest

@pytest.mark.parametrize(
    "nums,target,expected",
    [
        ([2,5,6,0,0,1,2], 0, True),
        ([2,5,6,0,0,1,2], 3, False),
        ([2,2,2,2,0,1,2], 3, False),
        ([3, 1], 1, True),
    ]
)
def test_search_in_rotated_array(nums, target, expected):
    s = Solution()
    a = s.search(nums, target)
    assert a == expected

if __name__ == "__main__":
    pytest.main(['-v', '-s'])