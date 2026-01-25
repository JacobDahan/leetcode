from typing import List

class Solution:
    """
    A conveyor belt has packages that must be shipped from one port to another within days days.

    The ith package on the conveyor belt has a weight of weights[i]. Each day, we load the ship with packages on the conveyor belt (in the order given by weights). We may not load more weight than the maximum weight capacity of the ship.

    Return the least weight capacity of the ship that will result in all the packages on the conveyor belt being shipped within days days.    
    """

    def shipWithinDays(self, weights: List[int], days: int) -> int:
        """
        Task:
        - We are given an array of packages with weights weights (where the weight of package i is equal to weights[i])
        - We must load all the packages, IN ORDER, onto a ship that has a specific weight capacity within days days
        - We are tasked with finding the MINIMUM weight capacity that would allow us to ship all the packages
        - We may not load more weight in any day than the weight capacity (assume that the ship delivers the packages between days)

        Observations:
        - We can easily GUESS a value capacity and evaluate if it is possible to ship all of the packages within days days
        - The capacity is BOUNDED:
            - We will NEVER be able to ship the packages if the capacity is smaller than the maximum package weight in weights
            - We will ALWAYS be able to ship the packages if the capacity is equal to the sum of the package weights
        - In other words, we have an answer space [max(weights), sum(weights)], which is naturally ordered, and trivial to "guess and check"
        - This is a perfect use case for binary search (MINIMIZATION, BOUNDARY CONVERGENCE)

        Algorithm:
        - Use binary search to find the minimum capacity along [max(weights), sum(weights)] that satisfies the predicate canDeliverPackages
        - Predicate: Use a greedy algorithm to deliver maximum weight in each day; when weight surpasses capacity, it must take another day; if the total days
            is less than or equal to days days, return True, otherwise False
        - Invariant: All values i, i < lo must NOT satisfy the predicate; all values i, i >= hi MUST satisfy the predicate
        - Termination: When lo == hi, we have definitionally found the convergence boundary where i is the first value that satisfies the predicate
        - Put in simple terms: We are looking for the BOUNDARY where the predicate transitions from FALSE to True
            - We can use binary search because we know that if capacity = c can ship in days days, so can capacity = c + 1;
              similarly, if capacity = c can NOT ship in days days, capacity = c - 1 CAN NOT EITHER
        """
        # first, find the maximum package weight (lo) and sum of package weights (hi) to define our search space
        lo, hi = 0, 0
        for weight in weights:
            lo = max(lo, weight) # no negative package weights, so we'll always find a non-zero package weight
            hi += weight # increment the sum
        
        # next, define our predicate evaluator
        def can_deliver_packages(capacity: int) -> bool:
            days_loading_packages = 1
            daily_cargo = 0

            for weight in weights:
                if daily_cargo + weight > capacity:
                    days_loading_packages += 1 # we've filled the ship for one day, we need to wait untilt he next day to keep loading
                    daily_cargo = 0 # on the next day, we've loaded nothing
                
                if days_loading_packages > days:
                    return False # return early if we've already exhausted the days we have at hand

                daily_cargo += weight

            return True # we've loaded all the packages and we didn't exhaust the days allowed!

        while lo < hi: # why not equals? because when lo == hi, we've found our boundary -- the invariant guarantees that all values GTE hi are valid answers
            mid = lo + (hi - lo) // 2 # avoid int overflow (not an issue in Python)

            if can_deliver_packages(mid):
                # this is a valid solution, but perhaps not the MINIMUM solution
                # per the invariant, set hi = mid to indicate this may be the answer, but keep searching
                # remember: if capacity = mid can deliver packages, so can all capacity > mid
                hi = mid
            else:
                # this is NOT a valid solution and must be discarded
                # remember: if capacity = mid can NOT deliver packages, neither can any capacity < mid
                lo = mid + 1
        
        return lo # lo == hi, and all values i, i >= hi are valid, so this MUST be the MINIMAL valid answer

# Test case: weights = [1,2,3,4,5,6,7,8,9,10], days = 5
# iter 1: lo = 10, hi = 55, mid = 32 // can_deliver = True
# iter 2: lo = 10, hi = 32, mid = 21 // can_deliver = True
# iter 3: lo = 10, hi = 21, mid = 15 // can_deliver = True
# iter 4: lo = 10, hi = 15, mid = 12 // can_deliver = False
# iter 5: lo = 13, hi = 15, mid = 14 // can_deliver = False
# iter 6: lo = hi = 15 // return 15

# Test case: weights = [1,2,3,1,1], days = 4
# iter 1: lo = 3, hi = 8, mid = 5 // can_deliver = True
# iter 2: lo = 3, hi = 5, mid = 4 // can_deliver = True
# iter 3: lo = 3, hi = 4, mid = 3 // can_deliver = True
# iter 4: lo = hi = 3 // return 3

import pytest

@pytest.mark.parametrize(
    "weights,days,expected",
    [
        ([1,2,3,4,5,6,7,8,9,10], 5, 15),
        ([1,2,3,1,1], 4, 3),
        ([3,2,2,4,1,4], 3, 6),
        ([1000, 1], 2, 1000),
    ]
)
def test_ship_within_days(weights, days, expected):
    s = Solution()
    a = s.shipWithinDays(weights, days)
    assert a == expected

if __name__ == "__main__":
    pytest.main(['-v','-s'])