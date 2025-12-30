class Solution:
    # Given a sorted integer array arr, two integers k and x, return the k closest integers to x in the array. 
    # An integer a is closer to x than an integer b if:
    #   |a - x| < |b - x|, or
    #   |a - x| == |b - x| and a < b

    def findClosestElements(self, arr: List[int], k: int, x: int) -> List[int]:
        # Take the simplest case (k = 1):
        # We can use binary search to find the nearest element to x in the array, specifically
        # - if arr[mid] >= x and mid > 0 and abs(arr[mid] - x) >= abs(arr[mid - 1] - x) --> look left, we have better answer
        # - elif arr[mid] >= x --> bring right and left to mid, this is our best answer
        # - elif arr[mid] < x and mid < len(arr) - 1 and abs(arr[mid] - x) >= abs(arr[mid + 1] - x) --> look right, we have better answer
        # - else --> bright left to right, this is our best answer

        left, right = 0, len(arr) - 1
        while left < right:
            mid = left + ((right - left) // 2)
            curr = arr[mid]

            if curr >= x and mid > 0 and abs(arr[mid] - x) >= abs(arr[mid - 1] - x):
                # Look left; there is a better answer to our left
                right = mid
            elif curr >= x:
                # Bring right and left to mid; this is our best answer
                # (mid is either equal to zero, or the next smallest number is so much smaller that it is further)
                right = left = mid
            elif curr < x and (abs(arr[mid] - x) > abs(arr[mid + 1] - x) or arr[mid] == arr[mid + 1]):
                # Look right; there is a better answer to our right
                left = mid + 1
            else:
                # Bring right and left to mid; this is our best answer
                # (mid is closer to x than the next largest number)
                right = left = mid
        
        # L = R at this point, pointing to the closest value
        # Next, we need to find the k closest neighbors
        # We can simply "fan out" from this index, comparing L and R neighbors to find the next closest
        while k > right - left + 1:
            if left == 0:
                # We can only grab from right
                right += 1
            elif right == len(arr) - 1:
                # We can only grab from left
                left -= 1
            elif abs(arr[left - 1] - x) <= abs(arr[right + 1] - x):
                # Left neighbor is closer
                left -= 1
            else:
                # Right neighbor is closer
                right += 1
        
        return arr[left:right + 1] # Include RHS