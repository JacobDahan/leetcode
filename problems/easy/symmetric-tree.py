# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def isSymmetric(self, root: Optional[TreeNode]) -> bool:
        # We can do this iteratively or recursively
        # Iterative approach:
        # - A tree is only symmetric if every "level" of the tree is mirrored
        # - When we want to process level by level, we should always think BFS
        # - In other words, search each level and build a list of nodes in that level;
        #   if that list of nodes is not equal to its reverse, then return false, else process next level
        # return self.isSymmetricIterative(root)
        # Recursive approach:
        # - A tree is only symmetric if every sub-tree is symmetric
        # - That is, we can recursively check every node in the tree
        # - A node is only symmetric if it has no children, or two children such that the LHS of the L child
        #   is equal to the RHS of the R child, and vice versa
        # - If any node is not symmetric, the tree may not be symmetric
        return self.isSymmetricRecursive(root.left, root.right)

    def isSymmetricIterative(self, root: Optional[TreeNode]) -> bool:
        if not root:
            return True
        
        # BFS requires a queue data structure (first-in, first-out)
        # We process each level one at a time, and validate that that level is a mirror of itself
        # If at any point we find a level that is not symmetric, we return false
        from collections import deque
        queue = deque([root])

        while queue:
            level = []
            # The number of nodes at any level of the queue can be determined simply by checking the queue len
            # here (e.g., len == 1 at the root node, len == n_child_nodes for its children, etc.)
            for _ in range(0, len(queue)):
                curr = queue.popleft()

                if not curr:
                    level.append(None)
                    continue
                
                level.append(curr.val)
                queue.append(curr.left)
                queue.append(curr.right)
        
            if level != level[::-1]:
                return False
        
        return True
                

    def isSymmetricRecursive(self, l_node: Optional[TreeNode], r_node: Optional[TreeNode]) -> bool:
        if not l_node and not r_node:
            # This is the simplest mirror: None is a clear mirror of None!
            return True
        
        if not l_node or not r_node:
            # If only one child is None, we cannot have a symmetric node
            return False
        
        if l_node.val != r_node.val:
            # If the two nodes themselves are not equal, don't bother checking children
            return False
        
        return self.isSymmetricRecursive(l_node.left, r_node.right)\
            and self.isSymmetricRecursive(l_node.right, r_node.left)