class Solution:

    # Given a non-negative integer x, return the square root of x rounded down to the nearest integer. 
    # The returned integer should be non-negative as well.
    # You must not use any built-in exponent function or operator.
    def mySqrt(self, x: int) -> int:
        if x == 0:
            return x
        
        if x < 4:
            return 1
        
        # By definition, for any value x > 4, the square root is maximally x // 2
        # (think: 4 --> 2; 5 --> 2; 6 --> 2; 7 --> 2; 8 --> 2, etc.)
        # Therefore our search bounds for the answer are strictly [2, x // 2]
        left = 2
        right = x // 2
        result = -1

        while left <= right:
            mid = left + ((right - left) // 2)
            val = mid * mid

            # If the value is greater than x, it is not a valid answer, and we must look to the left
            if val > x:
                right = mid - 1
            # If the value is less than x, it is a valid answer, but may not be optimal, so we must look to the right
            elif val < x:
                result = mid
                left = mid + 1
            # We found an exact answer, return
            else:
                return mid
        
        return result