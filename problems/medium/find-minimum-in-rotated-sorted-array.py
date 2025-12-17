class Solution:
    # Suppose an array of length n sorted in ascending order is rotated between 1 and n times.
    # Given the sorted rotated array nums of unique elements, return the minimum element of this array.
    def findMin(self, nums: List[int]) -> int:
        # brute force
        min = float('inf')
        for num in nums:
            if num < min:
                min = num
        return min