# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def hasPathSum(self, root: Optional[TreeNode], targetSum: int) -> bool:
        # What is this problem asking?
        # - *DOES* such a root-to-leaf path exist?
        # - We do not care about the shortest path, we do not need to find all occurrences
        # - All that we need to do is search root to leaf and calculate the sum; we don't need level-order
        # - This matches DFS well
        #   - DFS searches explicitly root-to-leaf, allowing us to quickly find our answer, or rule out branches
        #   - BFS needs to hold many partial calculations in memory ("bookkeeping") (adding node, remainingSum)
        #   - BFS is not just harder to code, but requires more memory (worst case O(n), versus O(log n) for DFS)
        
        # Alogrithm:
        # - set sum to zero
        # - add root val, if root exists
        # - calculate new targetSum (targetSum - sum)
        # - if root has child nodes, call hasPathSum(root.child, newTargetSum)
        # - else, return newTargetSum == 0
        if not root:
            return False
        
        # if not root.left and not root.right:
        #     # This is a leaf node, validate if we have found our target
        #     return targetSum - root.val == 0
        
        # # This is not a leaf node, check its children
        # return self.hasPathSum(root.left, targetSum - root.val) or\
        #     self.hasPathSum(root.right, targetSum - root.val)
        return self.hasPathSumIterative(root, targetSum)
    
    def hasPathSumIterative(self, root: Optional[TreeNode], targetSum: int) -> bool:
        # We can also solve this iteratively, since it's a basic DFS...
        # DFS uses a stack (last-in, first-out)
        stack = [(root, targetSum)]
        while stack:
            curr, remainder = stack.pop()
            remainder -= curr.val
            
            if not curr.left and not curr.right:
                # This is a leaf, return True if we've found a solution
                if remainder == 0:
                    return True
            
            # This is not a leaf node, add the children that exist
            if curr.left:
                stack.append((curr.left, remainder))
            if curr.right:
                stack.append((curr.right, remainder))
        
        # If we've made it here, we've checked every leaf node
        return False