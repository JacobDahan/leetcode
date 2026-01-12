class Solution:
    """
    A conveyor belt has packages that must be shipped from one port to another within days days.

    The ith package on the conveyor belt has a weight of weights[i].

    Each day, we load the ship with packages on the conveyor belt (in the order given by weights). 
    We may not load more weight than the maximum weight capacity of the ship.

    Return the least weight capacity of the ship that will result in all the packages on the conveyor belt being shipped within days days.
    """

    def shipWithinDays(self, weights: List[int], days: int) -> int:
        """
        Task:
        - We are given an integer array weights where the ith package has weights[i]
        - Each day, ships are loaded up to (not exceeding) capacity
        - We are asked to determine the MINIMUM weight capacity of the ship such that ALL the packages can be shipped in days days

        Observations:
        - It is *trivial* (i.e., O(w)) to determine if, for a given weight W, all packages can be shipped in days days
        - In other words, if we "guess" a weight W, we can easily verify if it is valid
        - If a ship with weight capacity W can ship all packages in days days, any ship with capacity X, X > W can, too
        - If a ship with weight capacity W cannot ship all packages in days days, any ship with capacity X, X < W cannot, either

        Binary Search:
        - Taken together, we have a SORTED ANSWER DOMAIN within which we can discard one side of the answer domain at each step,
          based on trivial (inexpensive) calculations
        - We are SEARCHING for the FIRST VALUE W to satisfy a predicate, in other words, this is a BOUNDARY SEARCH (minimization)
          binary search problem
            - Predicate: Can a ship with capacity W transport all packages in days days?
            - Invariant: For all W < lo, W does not satisfy the predicate; for all W >= hi, W does satisfy the predicate
        - But how can we define the bounds for W?
            - We can never transport all of the packages unless we can hold the heaviest package (W_min = max(weights))
            - In the worst case, we will need to carry all of the packages in a single day (W_max = sum(weights))
        """

        lo, hi = max(weights), sum(weights)

        def can_ship_within_days(w):
            """
            Utility method to determine if the provided weight satisfies the binary search predicate:
            Can a ship capable of bearing weight w ship packages of weights weights in days days?
            """
            weight_remaining, days_required = w, 1
            # We know packages are loaded in order and can't be split
            # Use a greedy algorithm to maximally fill the boat each day
            # If adding the weight would push us past capacity, we'll require an additional day to ship things
            for package in weights:
                if weight_remaining - package < 0:
                    days_required += 1
                    weight_remaining = w

                    if days_required > days:
                        return False # we only have days days, so no way this weight will work!
            
                weight_remaining -= package

            # we fit all the packages in d <= days! if we can do it in d days, we are guaranteed we can do it days days
            return True

        while lo < hi: # we continue searching until lo == hi; given our invariant, we know that we found the boundary where the predicate STARTS becoming true
                       # because our answer space is monotonically increasing, we are guaranteed this is the minimum value
            
            midpoint = lo + (hi - lo) // 2 # Python has no int overflow, but use the correct pattern here for practice

            if can_ship_within_days(midpoint): # because we check this at every iteration, binary search becomes O(p log S) where S = sum(weights) and p = len(weights)
                # this is a valid answer, but may not be the MINIMUM answer
                # we know all values greater than midpoint are valid, so there's no reason to keep them in our search space
                # but we keep this answer in case this IS the boundary where the predicate becomes true
                hi = midpoint
            else:
                # this is not a valid answer, so discard it and any weights less (no ship bearing less can satisfy the predicate)
                lo = midpoint + 1
        

        return lo # return the boundary, which is guaranteed to be the minimum value satisfying our predicate