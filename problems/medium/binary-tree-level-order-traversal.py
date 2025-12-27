from collections import deque

# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        if not root:
            return []
        
        level = 0
        queue, output = deque([root]), []

        while queue:
            if len(output) == level:
                output.append([])

            nodes_at_level = len(queue)
            for _ in range(0, nodes_at_level):
                node = queue.popleft()
                output[level].append(node.val)
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
                
            level += 1

        return output