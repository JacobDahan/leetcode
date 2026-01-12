class Solution:
    """
    Given an integer array nums and an integer k, split nums into k non-empty subarrays such that the largest sum of any subarray is minimized.

    Return the minimized largest sum of the split.

    A subarray is a contiguous part of the array.
    """

    def splitArray(self, nums: List[int], k: int) -> int:
        """
        Task:
        - Given an integer array numns and an integer k, we must split nums into k sub-arrays
        - The goal is to minimize the larget sum of any of the k sub-arrays
        - In other words, we find the most "balanced" division of sub-arrays

        Observations:
        - A sub-array is a contiguous part of the array, so forming sub-arrays is relatively trivial
        - The minimum "maximum" that we may ever return is the maximum of the list
            - That is, no minimum maximum sum can ever be smaller than taking the largest element and putting it in its own array
        - The maximum maximum that we could ever return would be the sum of the elements in the list (put all the elements in one sub-array and call it a day)
        - Therefore, we have a bounded answer space of [max(nums), sum(nums)]
        - What can we do with this answer space?
            - Well, for each answer, we could check if there's a valid solution! Starting at max(nums) and going up...
            - We can define is_valid(minimized_max_sum) := [for each element in nums, add to current sub-array if curr_sum + element <= minimized_max_sum; else next sub-array]
            - Once we find an answer, since we started at the "bottom end" of the answer space, we know it's the minimum!
            - ... But what if the sum(nums) is *huge*? We can search more efficiently using binary search over the answer space!

        Binary Search:
        - Binary search allows us to discard half of the answer space at each step
            - We know that for any "minimized_max_sum" satisfying the predicate, all values mms > minimized_max_sum will also satisfy our is_valid predicate
                - i.e., if we can minimize the sums to 10, we can also minimize the sums to 100
            - We know that for any "minimized_max_sum" NOT satisfying the predicate, all values mms < minimized_max_sum will also NOT satisfy our is_valid predicate
                - i.e., if we cannot minimize the sums to 100, we cannot minimize the sums to 10
            - With these conditions met, we can assertively keep or throw away half of the answer space with each is_valid check
        - Traditionally, binary search is O(n) runtime (n = size of answer space), but here we need to iterate over nums at each loop, resulting in O(m log n) runtime
          (where n is the *sum* of nums, since that defines our search range)
        - This is still O(1) space

        So how do we execute the binary search?
        - This is a classic boundary search, minimization problem: We want to find the "least big" number that satisfies our predicate (first true)
        - Predicate: For a given answer, can we create contiguous sub-arrays such that all of the sums are equal to or less than the answer?
        - Invariant: For any i, i < lo, the predicate must not be satisfied; for any i, i >= hi, the predicate mut be satisfied
        - At each step, if the answer is valid, we set hi = answer (keeping our invariant true), else we reject this answer and all answers lower than it from the answer space
        """
        lo, hi = max(nums), sum(nums)
        
        def is_valid(answer: int) -> bool:
            """
            Utility method to determine if a given answer satisfies the following predicate:
            Can the array nums be divided into contiguous sub-arrays such that no sum of any sub-array is greater than the answer?
            """
            running_sum, sub_array_count = answer, 0
            for number in nums:
                if running_sum - number < 0: # this value can't fit in this sub-array, move to the next
                    sub_array_count += 1
                    running_sum = answer

                    if sub_array_count == k: # if we've exhausted all our sub-arrays, this is NOT a valid answer
                        return False

                running_sum -= number # this number CAN fit in this sub-array, guaranteed, because the sub-arrays are minimially the maximum size of nums
            
            return True # if we've made it here, we managed to fit all our numbers in the available arrays!

                
        
        while lo < hi: # note we use lo < hi because when lo == hi, we've found our answer!
            midpoint = lo + (hi - lo) // 2 # bias towards lower values (if mid == lo and is_valid, hi will be drawn down so we don't get stuck)

            if is_valid(midpoint):
                # this is a valid answer, but may not be the MINIMUM (first true) answer, so we look "left"
                # we keep this value, as it may be the answer, and set it to hi to maintain our invariant (all i >= hi satisfy predicate)
                hi = midpoint
            else:
                # this is not a valid answer
                # discard this answer and all answers lower than it, as those ALSO will not be valid answers (see our observations above)
                lo = midpoint + 1
        
        return lo

