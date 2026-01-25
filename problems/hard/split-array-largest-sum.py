from typing import List

class Solution:
    """
    Given an integer array nums and an integer k, split nums into k non-empty subarrays such that the largest sum of any subarray is minimized.

    Return the minimized largest sum of the split.

    A subarray is a contiguous part of the array.
    """

    def splitArray(self, nums: List[int], k: int) -> int:
        """
        Task:
        - We are given an integer array nums and an integer k
        - Our task is to split nums into k subarrays such that the LARGEST SUM of any subarray is MINIMIZED
        - A subarray must be a contiguous part of the array

        Observations:
        - For any value l := largest_sum, it is trivial to evaluate if it is possible to split nums into k or fewer sub-arrays with largest sum l
        - For any value l := largest_sum that can be satisfied, all values i, i > l MUST also satisfy the predicate
        - For any value l := largest_sum that cannot be satisfied, all values i, i < l MUST NOT satisfy the predicate (think: If we can't split an array into chunks of size <= 10, how could we for 9?)
        - The values largetst_sum are a continuous, naturally ordered, duplicate free array
        - With these conditions, we can use binary search along the answer space to find the BOUNDARY CONVERGENCE POINT where the predicate STARTS TO BECOME SATISFIED (minimization)

        Algorithm:
        - largest_sum may not be smaller than the maximum of max(nums) (all elements must fit) and sum(nums) // k (perfect packing)
        - largest_sum must satisfy the predicate where l = sum(nums) (we can of course split into arrays of size total_size or smaller!)
        - Therefore, perform binary search along [sum(nums) // k, sum(nums)]
        - Invariant: For any value i, i < lo, the predicate must not be satisfied; for any value i, i >= hi, the predicate must be satisfied
        - Termination condition: When lo == hi, we have definitionally found our boundary condition -- the first value to satisfy the predicate
        - Predicate: We can simply form contiguous sub-arrays up to a maximum sum of largest_sum, and return True if we can fit into k or fewer sub-arrays
        """

        lo, hi = max(sum(nums) // k, max(nums)), sum(nums)

        def can_split_with_sum_or_smaller(sum: int) -> bool:
            sub_arrays_in_use = 1
            sub_array_sum = 0

            for num in nums:
                if sub_array_sum + num > sum:
                    # we'd overflow this sub-array by adding another element, so move to the next
                    sub_arrays_in_use += 1
                    sub_array_sum = 0
                
                if sub_arrays_in_use > k:
                    # exit early, we can't fit into sub-arrays of size sum
                    return False
                
                sub_array_sum += num
            
            return True

        while lo < hi: # why not equals? our invariant guarantees that when lo == hi we've found the first value that satisfies the predicate
            mid = lo + (hi - lo) // 2 # avoid int overflow, even though it's not possible in Python

            if can_split_with_sum_or_smaller(mid):
                # this value satisfies the predicate and may be our answer, but there MAY exist a better solution (smaller maximum sum)
                # we know that any value > mid also satisfies this, so we set hi = mid to satisfy our invariant
                hi = mid
            else:
                # this value does not satisfy the predicate and must not be our answer
                # all smaller values ALSO must not be our answer, so discard those as well
                lo = mid + 1
        
        return lo