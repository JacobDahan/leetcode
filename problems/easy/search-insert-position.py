class Solution:
    def searchInsert(self, nums: List[int], target: int) -> int:
        """
        Given a sorted array of distinct integers and a target value, return the index if the target is found. 
        If not, return the index where it would be if it were inserted in order.
        
        You must write an algorithm with O(log n) runtime complexity.
        """
        # We are given a sorted array and asked to search for a target value.
        # If the target value does not exist, we must return the index where the target would be inserted.
        # In other words, we are looking for the first index (smallest value) such that nums[i] >= target.
        # We are given the additional hint that we are looking for a O(log n) runtime complexity answer.
        # This screams binary search!

        # There are two forms of binary search and we can easily use either for this problem.
        # Form 1: Search with closed bounds.
        # - In this form, we search along [lo, hi] where the answer must lie between lo and hi if it exists.
        # - Both lo and hi are potential answers (meaning we must consider the case lo == hi),
        #   and we check the mid at each step
        # - If mid is not a valid answer, we must remove it from the search space, as the invariant dictates
        #   that the solution must live within [lo, hi] (if it exists)
        # - If lo > hi, the answer does not exist in the search space -- this means that target is not in the
        #   array. Because lo was always pointing at a potential answer while looping, it must now be pointing
        #   at the first value bigger than target (or len(nums) if no such value exists)
        # lo, hi = 0, len(nums) - 1
        # while lo <= hi:
        #     mid = lo + ((hi - lo) // 2) # avoid int overflow
        #     val = nums[mid]
            
        #     if val == target:
        #         return mid
            
        #     if val > target:
        #         # this is not the target, and so must be removed from the search space
        #         # (we look left to find the smaller target)
        #         hi = mid - 1
        #     else:
        #         # this is not the target, and so must be removed from the search space
        #         # (we look right to find the bigger target)
        #         lo = mid + 1
        
        # # If we reach here, the target is not in the array
        # # By nature of our invariant (lo is always pointing at a potential answer), lo must now point at the
        # # first value greater than the target -- the index where the target would be inserted
        # return lo

        # Form 2: Boundary convergence
        # - This problem can be more naturally re-framed as boundary convergence
        # - That is, we are not checking midpoints to find the answer, but trying to narrow our search space
        #   to find when a condition becomes true -- when nums[i] >= target
        # - The invariant here is that all values i < lo do not satisfy the condition, and all values >= hi
        #   satisfy the condition (i.e., the valid search space is [lo, hi))
        # - When lo == hi, the bounds [lo, hi) is empty and the answer must be lo (the first index where the condition
        #   is true)
        lo, hi = 0, len(nums) # we use len(nums) here because hi is exclusive
        while lo < hi:
            mid = lo + ((hi - lo) // 2)
            val = nums[mid]

            if val >= target:
                # This is a valid answer, and therefore we need to keep it (definitionally, all values
                # >= hi satisfy the condition)
                hi = mid
            else:
                # This is not a valid answer, remove it from the search space so that the boundary converges
                # towards the answer
                lo = mid + 1
        
        return lo