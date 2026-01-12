class Solution:
    """
    You are given an m x n integer matrix matrix with the following two properties:

    Each row is sorted in non-decreasing order.
    The first integer of each row is greater than the last integer of the previous row.

    Given an integer target, return true if target is in matrix or false otherwise.

    You must write a solution in O(log(m * n)) time complexity.
    """

    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        """
        Observations:
        - We are asked to SEARCH for an element in an ordered matrix
        - We are asked to write a solution in O(log(m * n)) time
        - When we are asked to SEARCH an ordered array or similar, we should think binary search
        - Binary search executes with logarithmic runtime complexity because we can discard half the search space on each "step"

        Binary Search:
        - How can we binary search a matrix?
            - We are told that each row is sorted in non-decreasing order
            - We are told that the first integer of each row is greater than the last integer of the previous row
        - In other words, the *columns* are monotonically increasing, and the rows are non-decreasing
        - Trivially, we can determine the row that contains the target (if it exists) (O(log m))
        - After that, we can perform a second binary search in that row to find the element (O(log n))
        - By logarithmic rules, the total time (O(log m) + O(log n)) is equivalent to that requested:  O(log(m * n))

        (Technically, we could do this in one binary search by using floor division and modulos to "find" our row and column, but it's exactly the same number of searches...)
        """
        # return self.searchInOne(matrix, target)
        return self.searchInTwo(matrix, target)

    def searchInOne(self, matrix: List[List[int]], target: int) -> bool:
        # basic edge cases
        if not matrix or not matrix[0]: # no elements, no match!
            return False
        
        m, n = len(matrix), len(matrix[0])

        # we can execute this in a single binary search with runtime O(log m * n) by "pretending" this is a flat array
        # we just need to find our "index"
        # - we search the range [0, (m * n) - 1]
        # - the index i represents row i // n and column i % n
        lo, hi = 0, (m * n) - 1
        while lo <= hi:
            midpoint = lo + (hi - lo) // 2
            row, column = midpoint // n, midpoint % n # for example, in [[1, 2], [3, 4]], midpoint 1 would be at (0, 1)
            val = matrix[row][column]
            if val == target:
                return True
            
            if val > target:
                # this value, all values right of this in the row, and all later rows are NOT going to contain target
                # discard these from the search space and continue
                hi = midpoint - 1
            else:
                # this value, all values left of this in the row, and all previous rows are NOT going to contain target
                # discard these from the search space and continue
                lo = midpoint + 1

        return False # no match!
    
    def searchInTwo(self, matrix: List[List[int]], target: int) -> bool:
        # basic edge cases
        if not matrix or not matrix[0]: # no elements, no match!
            return False
        
        if matrix[0][0] > target: # if all elements are greater than target, no match!
            return False
        
        m, n = len(matrix), len(matrix[0])


        # First, search the matrix to discover which row the target exists in, if it exists
        # Here, we are trying to find the LAST row where matrix[row][0] <= target
        # In other words, we are trying to find the boundary where last element satisfying a given predicate is true
        # - Predicate: matrix[row][0] <= target
        # - Invariant: For all row <= lo, the predicate must be true; for all row > hi, the predicate must be false
        lo, hi = 0, m - 1
        while lo < hi: # when lo == hi, we find the LAST row where this predicate is met
            row = lo + (hi - lo + 1) // 2 # we bias towards the *higher* end of the spectrum to avoid getting "stuck" when lo == row and first_val <= target
                                          # consider the case [1, 2] where lo = 0, hi = 1, and target = 2; we'd be stuck setting lo = row = 0 and never progress 
            first_val = matrix[row][0]

            if first_val <= target:
                # it is POSSIBLE that the target exists in this row, but there may be a further row that satisfies our predicate
                # regardless, we know that this and all rows before this satisfy our predicate, so move our search window
                lo = row
            else:
                # it is NOT POSSIBLE that the target exists in this row, nor any row beyond this
                # discard this row and all others beyond this from the search space
                hi = row - 1
        
        row = lo

        # Second, search in the found row for the target
        # Again, we use binary search, but in a different form
        # - Invariant: If the target exists in row, it must exist along [lo, hi]
        lo, hi = 0, n - 1
        while lo <= hi: # the target may exist anywhere along [lo, hi], including lo == hi, but this is not guaranteed
                        # we have to explicitly check when the two are equal
            
            column = lo + (hi - lo) // 2 # no need to bias higher; but things would still work if we did! we can't get stuck in range elimination variant
            val = matrix[row][column]

            if val == target:
                return True
            
            if val > target:
                # val is greater than target, as are all values to the right of val
                # look left and discard all values right
                hi = column - 1
            else:
                # val is less than target, as are all values to the left of val
                # look right and discard all values left
                lo = column + 1
        
        # if we made it here, there are no matches!
        return False