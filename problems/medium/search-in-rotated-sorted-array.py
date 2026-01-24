from typing import List

class Solution:
    """
    There is an integer array nums sorted in ascending order (with distinct values).

    Prior to being passed to your function, nums is possibly left rotated at an unknown index k (1 <= k < nums.length) such that the resulting array is [nums[k], nums[k+1], ..., nums[n-1], nums[0], nums[1], ..., nums[k-1]] (0-indexed). 
    
    For example, [0,1,2,4,5,6,7] might be left rotated by 3 indices and become [4,5,6,7,0,1,2].

    Given the array nums after the possible rotation and an integer target, return the index of target if it is in nums, or -1 if it is not in nums.

    You must write an algorithm with O(log n) runtime complexity.
    """

    def search(self, nums: List[int], target: int) -> int:
        """
        Task:
        - We are given an array that is POSSIBLY rotated at an index k (1 <= k < nums.length)
        - We are asked to find an integer target in that array
        - The integer may or may not exist; if exists, return its index, otherwise -1

        Observations:
        - For our algorithm, we can assume that k always exists and 0 <= k < nums.length, where rotation at k = 0 returns the original array
        - Following rotation, we have an array that is ordered but not strictly sorted
            - That is, the array is comprised of two sorted sub-arrays
            - At any given index i, the sub-array to the left of i will be sorted, or the sub-array to the right of i will be sorted, or both
                - For example, in [4,5,6,7,0,1,2], if we pick index i = 1, all elements left are sorted (there is only one) whereas the sub-array to the right is not sorted
                - In the same array, if we pick index i = 5, all elements left of i are sorted, as are all elements right of if
        - How does this help us?
            - We are asked to find an integer in an array, and explicitly told to use O(log n) runtime complexity
            - This screams binary search!
            - Binary search achieves its logarithmic time complexity because we can make assertions about the possibility of a number existing to one side
              of our search index or the other
            - Typically, we can make those assertions because we execute binary search on sorted arrays, so it's trivial to say "does X fall along [Y, Z]"
            - Here, we do not necessarily have a sorted array, but we can always determine if the value at index i MAY POSSIBLY fall between the bounds of
              whichever SUB ARRAY is sorted
            - In other words, we can only make assertions about one side of the array at a time, but that still lets us cut the search space in half at each iteration
        
        Algorithm:
        - Use binary search on the partially sorted array
        - Invariant: If target exists in nums, it must fall along [lo, hi]
        - Search space: We must search all values along [lo, hi], including when lo == hi, because the invariant does not guarantee that lo == hi will give us a valid answer
        - Termination: When lo and hi cross over, we have exhausted our search space, and target may not exist in nums
        - For each "mid" index i, check whether the left or right sub array is sorted -- one is always guaranteed to be so
        - Once the sorted sub-array is found, discard if target does not fall within its bounds, else discard the other!
        """
        lo, hi = 0, len(nums) - 1 # every element in the array is a valid part of the search space to start

        while lo <= hi: # why equals? the invariant does not guarantee that we have a solution when lo == hi, so we must evaluate this index, too
            mid = lo + (hi - lo) // 2 # Python does not have int overflow, but take care in case we switch languages...
            
            if target == nums[mid]:
                # we found our target! stop searching and return
                return mid
            
            # we didn't find our target, cut the search space in half
            
            if nums[mid] >= nums[lo]:
                # the LHS must be strictly ascending (remember: we rotated a sorted array, so if we are looking left across the rotation point, we are looking at BIGGER numbers)
                if target < nums[mid] and target >= nums[lo]:
                    # the target must lie between lo and mid if it exists in the array, so discard the RHS
                    hi = mid - 1
                else:
                    # the target must NOT lie between lo and mid, so discard the LHS
                    lo = mid + 1
            else:
                # if the LHS is not sorted, then the RHS MUST be (the rotation axis is between mid and lo if lo > mid)
                if target > nums[mid] and target <= nums[hi]:
                    # the target must lie between mid and hi if it exists in the array, so discard the LHS
                    lo = mid + 1
                else:
                    # the target must NOT lie between mid and hi, so discard the RHS
                    hi = mid - 1
        
        # when lo > hi, we've exhausted the entire search space
        # target may not possibly exist in nums
        return -1

# [4,5,6,7,0,1,2], 0
# lo = 0, hi = 6
# iter 1: lo = 0, hi = 6, mid = 3, val = 7 // 7 > 4 (sorted); 0 < 7, 0 < 4 (look right); lo = 4
# iter 2: lo = 4, hi = 6, mid = 5, val = 1 // 1 > 0 (sorted); 0 < 1, 0 <= 0 (look left); hi = 4
# iter 3: lo = 4, hi = 4, mid = 4, val = 0 // target found! return 4

import pytest

@pytest.mark.parametrize("input", "target", "expected", [
    ([4,5,6,7,0,1,2], 0, 4),
    ([4,5,6,7,0,1,2], 6, 2),
    ([4,5,6,7,0,1,2], 10, -1),
])
def test_search_in_once_rotated_array(input, target, expected):
    s = Solution()
    a = s.search(input, target)
    assert a == expected