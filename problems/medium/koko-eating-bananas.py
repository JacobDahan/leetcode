import math

class Solution:
    """
    Koko loves to eat bananas. There are n piles of bananas, the ith pile has piles[i] bananas. 
    
    The guards have gone and will come back in h hours.

    Koko can decide her bananas-per-hour eating speed of k. Each hour, she chooses some pile 
    of bananas and eats k bananas from that pile. If the pile has less than k bananas, she eats 
    all of them instead and will not eat any more bananas during this hour.

    Koko likes to eat slowly but still wants to finish eating all the bananas before the guards return.

    Return the minimum integer k such that she can eat all the bananas within h hours.
    """

    def minEatingSpeed(self, piles: List[int], h: int) -> int:
        """
        Observations:
        - We need to find the minimum banana eating speed (k) to eat n piles of bananas
        - Each pile i has piles[i] bananas
        - If a pile has less than k bananas, it still takes a full hour (e.g., k = 3, piles[i] = 1)
        - piles.length <= h

        What do we know?
        - k must be an integer, so to make progress k must be greater than or equal to 1
        - if k was equal to the maximum pile size, it would take len(piles) hours to consume all the bananas
            - Since h may be only as small as len(piles), it never makes sense to have k > max(piles)
        - therefore, k must be along [1, max(piles)]

        Binary Search
        - Since k must be along a defined and relatively small domain ([1, max(piles)]), and calculating whether
          k is sufficiently large for Koko to consume all bananas is an O(m) operation (m = len(piles)), and the search
          domain of ANSWERS is inherently ORDERED, we can use BINARY SEARCH ALONG THE ANSWER DOMAIN to find the answer
        - In other words, we can use binary search along the answer domain to find the minimum answer
            - This will be O(m * log n) runtime complexity (calculate the total banana consumption in m piles
              for each iteration of the binary search) and O(1) space complexity
            - Predicate: sum([math.ceil(pile / k) for pile in piles]) <= h
            - Invariant: all values k, k < lo must not satisfy the predicate; all values k >= hi must
        """
        lo, hi = 1, max(piles) # there is NEVER a reason to eat faster than max(piles) -- Koko is lazy!
        while lo < hi: # when lo == hi, our invariant demands that we've found the MINIMUM value k such that the
                       # predicate is satisfied

            midpoint = lo + (hi - lo) // 2 # no int overflow in Python, but good practice
            hours_to_consume = sum([math.ceil(pile / midpoint) for pile in piles])

            if hours_to_consume > h:
                # this is not a valid solution for k
                # per our invariant, all values that do not satisfy the predicate should be abandoned in
                # our search window, so move lo above this
                lo = midpoint + 1
            else:
                # this is a valid solution for k, but may not be OPTIMAL
                # per our invariant, we keep the "best" value we've found so far for k in our search window
                # so move hi to this value
                hi = midpoint
        
        return lo

