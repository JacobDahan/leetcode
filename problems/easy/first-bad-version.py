# The isBadVersion API is already defined for you.
# def isBadVersion(version: int) -> bool:

class Solution:
    def firstBadVersion(self, n: int) -> int:
        # n >= 1
        left, right = 1, n

        # We can solve this using binary search
        # However, unlike a "typical" problem where we return when we find our
        # target, this is effectively binary search with duplicates -- and we want
        # the first occurrence

        # How can we solve this? Well, when we find an answer, we don't return.
        # We must:
        # 1. Keep that answer inside our search area (in case there are no earlier answers)
        # 2. Continue searching until L and R converge (no more answers to check)
        # 3. Return L (or R, as they are overlapping)

        while left < right:
            mid = left + ((right - left) // 2)
            is_bad_version = isBadVersion(mid)

            # If this is a bad version, we must keep this version in our search area, but we also must
            # look for earlier bad versions, if they exist
            if is_bad_version:
                right = mid
            # If this is not a bad version, we do not need to keep this version in our search area,
            # and we must look for later versions
            else:
                left = mid + 1

        return left