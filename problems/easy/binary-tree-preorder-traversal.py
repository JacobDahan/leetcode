# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def preorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        if root is None:
            return []
        
        # The most trivial solution is a recursive solution -- the question asks us to work iteratively
        # return [root.val] + self.preorderTraversal(root.left) + self.preorderTraversal(root.right)

        # DFS asks us to use a STACK (last-in, first-out) to track the work we have left to do
        stack, result = [root], []
        while stack:
            node = stack.pop()

            # node is none, this is a dead-end
            if not node:
                continue

            # pre-oroder states that we must put the node value, then left, then right
            result.append(node.val)
            
            # to process left before right, we must push right before left (last-in, first-out)
            stack.append(node.right)
            stack.append(node.left)

        return result