# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        # If root is none, it adds nothing to the depth of the tree
        if not root:
            return 0
        
        # Bottom-up recursion:
        # Each node knows how deep it is by the answer of its children
        # The max depth of this node is simply 1 plus the maximum depth of its children
        # return 1 + max(self.maxDepth(root.left), self.maxDepth(root.right))
    
        # We can also do this top-down...
        # The max depth of this node is whatever the bottom node says it is!
        # return max(self.findMaxDepth(root.left, 1), self.findMaxDepth(root.right, 1))

        # Or we can do this iteratively...
        stack, answer = [(root, 1)], 0
        while stack:
            node, level = stack.pop()
            if level > answer:
                answer = level
            if node.left:
                stack.append((node.left, level + 1))
            if node.right:
                stack.append((node.right, level + 1))
        
        return answer
    
    # def findMaxDepth(self, root: Optional[TreeNode], answer: int) -> int:
        # if not root:
            # return answer
        
        # return max(self.findMaxDepth(root.left, answer + 1), self.findMaxDepth(root.right, answer + 1))
