# The guess API is already defined for you.
# @param num, your guess
# @return -1 if num is higher than the picked number
#          1 if num is lower than the picked number
#          otherwise return 0
# def guess(num: int) -> int:

# Constraints:
#    1 <= n <= 2^31 - 1
#    1 <= pick <= n


class Solution:
    def guessNumber(self, n: int) -> int:
        # We have to guess what `pick` is for any given `n`,
        # where 1 <= pick <= n. In other words:
        # - Search the entire space [1, n]
        # - Guess values in that space
        # - Adjust search based on guess(num: int) -> int results
        # Since a range of numbers is sorted by definition, we can use binary search


        # We have to search the space [1, n]
        left = 1
        right = n

        # The potential answer space is only what exists between L and R
        while left <= right:
            # Split the answer space
            mid = left + ((right - left) // 2)
            # Guess this number...
            result = guess(mid)
            # If we guessed right, return:
            if result == 0:
                return mid
            # If num > pick, we need to search to the left of our last guess
            elif result == -1:
                right = mid - 1
            # If num < pick, we need to search to the right of our last guess
            else:
                left = mid + 1

        # Should be unreachable, assuming the actual pick adheres to the assigned
        # bounds
        return -1