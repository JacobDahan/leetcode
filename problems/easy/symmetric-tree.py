from collections import deque

# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    # Iterative solution
    # def isSymmetric(self, root: Optional[TreeNode]) -> bool:
    #     if not root:
    #         return True

    #     # Thoughts:
    #     # - A tree is a mirror of itself if and only if every level of the tree
    #     #   is a mirror of itself
    #     # - Literally, a level is a mirror of itself if the list of nodes can be reversed without
    #     #   the level changing
    #     # - Since we are comparing level-by-level, this is appropriate for BFS
    #     # - Algorithm: Go one level at a time; if level.reversed() != level, return False; 
    #     #   if BFS completes, return True

    #     # BFS uses a queue data structure (first-in, first-out)
    #     queue = deque([root])
    #     while queue:
    #         # We know how many elements belong to this level by checking the length of the queue here
    #         # (e.g., at start, len(queue) == 1, then the n children of the root node, etc.)
    #         level = []
    #         for _ in range(0, len(queue)):
    #             curr = queue.popleft()
    #             if curr:
    #                 level.append(curr.val)
    #                 queue.append(curr.left)
    #                 queue.append(curr.right)
    #             else:
    #                 level.append(None)
            
    #         if level != list(reversed(level)):
    #             return False
        
    #     return True
    
    # Recursive solution
    def isSymmetric(self, root: Optional[TreeNode]) -> bool:
        # Thoughts:
        # - A tree is only a mirror of itself if the root node is a mirror of itself
        # - The root node is a mirror of itself if its left side is a mirror of its right side
        # - The left side is a mirror of the right side if its left side is equal to the right side's right side...
        # - In other words:
        #       isMirror(l_node, r_node) can be solved by recursively comparing the LHS of the l_node to the
        #       RHS of the r_node
        return self.isMirror(root.left, root.right)

    def isMirror(self, l_node: Optional[TreeNode], r_node: Optional[TreeNode]) -> bool:
        if not l_node and not r_node:
            # Easiest mirror: None == None
            return True
        
        if not l_node or not r_node:
            # If one is None and the other is not, this cannot be a mirror
            return False
        
        if l_node.val != r_node.val:
            # If the two nodes are not equal, it cannot be a mirror
            return False
        
        # Two nodes are only mirror nodes if the LHS of left is equal to the RHS of right, and vice versa...
        return self.isMirror(l_node.left, r_node.right) and self.isMirror(l_node.right, r_node.left)