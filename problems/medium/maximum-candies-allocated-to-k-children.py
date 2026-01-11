class Solution:
    """
    You are given a 0-indexed integer array candies. Each element in the array denotes a pile of candies of size candies[i]. 
    You can divide each pile into any number of sub piles, but you cannot merge two piles together.

    You are also given an integer k. You should allocate piles of candies to k children such that each child gets the same number of candies. 
    Each child can be allocated candies from only one pile of candies and some piles of candies may go unused.

    Return the maximum number of candies each child can get.
    """

    def maximumCandies(self, candies: List[int], k: int) -> int:
        """
        Goal:
        - We are given am array candies consisting of piles of candies (pile_size_i = candies[i])
        - We can sub-divide each pile into as many sub-piles as we want, but never merge piles
        - We are asked to allocate piles of candies to k children such that each child gets the same number of candies,
          where each child can take from only one pile of candies
        - In other words, find the maximum number of candies each child can get

        Observations:
        - The minimum candy each child can get is, of course, 0
        - The maximum candy any child can get is:
            - Trivially, the maximum is the maximum pile size, since no child can draw from more than one pile
            - More thoughtfully, the maximum is the sum of the candies divided by the number of children (a perfectly distributed set of piles)
        - These bounds [0, sum(piles) // k] are a monotonically increasing answer space, and a reasonably small one
        - For each answer, we can trivially check if it satisfies the predicate that each child may receive equal candy
        - Since the predicate will always be true for smaller numbers of candy (if we can subdivide 10 candies each, we can of course do 9),
          and eventually false for larger numbers of candy (if we can give 1 candy each, we cannot necessary do 1000), there must exist some boundary
          along our answer space where the predicate turns from not satisfied to satisfied
          - This means we are SEARCHING along a SORTED ANSWER SPACE for a predicate BOUNDARY -- this can be solved cleanly with binary search
          - We use the BOUNDARY CONVERGENCE form of binary search
            - Predicate: Can k children receive n candies each?
            - Invariant: For all values i <= lo, the predicate is satisfied; for all values i > hi, the predicate is not
            - This is the standard "MAXIMIZATION" form
        """
        lo, hi = 0, sum(candies) // k # recall the invariant:
                                      # lo = 0 --> we know that all children can (unhappily) get 0 candies (all i <= lo must satisfy predicate)
                                      # hi = sum(candies) // k --> equally distributing to all children would satisfy the predicate with a perfect
                                      # set of piles, but it will never be possible to distribute more candies than that to all children (all i > hi must
                                      # not satisfy the predicate)

        def is_valid(answer: int) -> bool:
            """
            Utility method to assess the predicate: Can k children receive n candies each?
            Returns True if the predicate is satisfied, else False.
            """
            kids_to_feed = k
            for pile in candies:
                kids_to_feed -= pile // answer # we can maximally allocate answer candies to `pile // answer` children equally
                                               # (e.g., in a pile of 10, we can only allocate to 3 children for answer = 3)
                if kids_to_feed <= 0:
                    return True
            
            return False
        
        while lo < hi: # recall the invariant: all values i <= lo are valid and all i > hi are not, so when lo == hi we've found the maximal value i
            midpoint = lo + (hi - lo + 1) // 2 # no int overflow in Python, but let's take care...
                                               # note that we use +1 for effective ceiling division -- we want to "bias" towards larger numbers, else our loop
                                               # may get stuck when midpoint == lo and lo is valid 
            if is_valid(midpoint): # because is_valid iterates maximally over m piles, the runtime complexity becomes O(m log n)
                # if this is a valid solution to the problem, keep it in the answer space
                # recall that all values i <= lo are valid; this is our "maximal answer" SO FAR
                lo = midpoint
            else:
                # if this is NOT a valid solution to the problem, it may not exist in the answer space
                hi = midpoint - 1
        
        return lo