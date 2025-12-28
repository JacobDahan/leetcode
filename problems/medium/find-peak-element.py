class Solution:
    def findPeakElement(self, nums: List[int]) -> int:
        # Thinking:
        # - We are asked to do this in O(log n) time, which suggests binary search
        # - But the array is not sorted, so how can we refine our search at each iteration?
        # - nums[i] != nums[i + 1] for all valid i.
        # - What is a local peak:
        #   - A peak element is an element that is strictly greater than its neighbors.
        #   - nums[-1] = nums[n] = -∞
        # - Therefore, for any index i:
        #   - If nums[i] > nums[i - 1], there must exist a peak [i, n) because either:
        #       1. nums[i] > nums[i + 1] (i is peak)
        #       2. nums[j] > nums[i] (j > i, j is peak) -- array is strictly increasing (last element is peak)
        #          or a standard peak exists to the right of i
        #   - If nums[i] < nums[i - 1], there must exist a peak [0, i) because either:
        #       1. nums[i - 1] > nums[i - 2] (i - 1 is peak)
        #       2. nums[j] > nums[i - 1] (j < i, j is peak) -- array is strictly decreasing (first element is peak)
        #          or a standard peak exists to the left of j

        left, right = 0, len(nums) - 1
        # We continue until left and right are pointing at the same value, at which point that value must be
        # our answer
        while left < right:
            mid = left + ((right - left) // 2)
            curr = nums[mid]

            if mid < len(nums) and curr < nums[mid + 1]:
                # If nums[i] < nums[i + 1], there must exist a peak (i, n)
                # Therefore, we drop the left index as a possible answer and discard everything left of it
                left = mid + 1
            else:
                # If nums[i] > nums[i + 1], there must exist a peak [0, i]
                # Therefore, we keep the midpoint and everything to the right of it
                right = mid
        
        return left