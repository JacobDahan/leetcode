class Solution:
    # Given a sorted integer array arr, two integers k and x, return the k closest integers to x in the array. 
    # An integer a is closer to x than an integer b if:
    #   |a - x| < |b - x|, or
    #   |a - x| == |b - x| and a < b

    def findClosestElements(self, arr: List[int], k: int, x: int) -> List[int]:
        # This is a sorted array: Think binary search
        # ... But we can't just search for an element, we are searching for a *slice*
        # What is our search condition?
        # We want to find the index i such that arr[i:i+k] gives us the minimum difference from x
        # At any given index i, we can determine whether the arr[i:i+k] or arr[i+1:i+k+1] slice is "better"
        # - If the former is a better solution, no values j, j >= k are valid (as it would imply we can't include i)
        # - If the latter is a better solution, no values j, j <= i are valid (as it would imply we include i)
        # - The "better" solution is just whichever is closer -- i, or k -- to x
        # - But what is "better" when two are equal? The leftmost answer
        left, right = 0, len(arr) - k # Left index can never be greater than this
        while left < right:
            mid = left + ((right - left) // 2)
            if x - arr[mid] > arr[mid + k] - x:
                # In other words, if x is larger than arr[mid] than arr[mid + k] is larger than x,
                # arr[mid + k] must be closer to x and we should look right
                left = mid + 1
            else:
                # Otherwise, x may be smaller than mid, or just closer to x than mid + k,
                # so we should look left
                right = mid
        
        # L == R
        return arr[left:left+k]