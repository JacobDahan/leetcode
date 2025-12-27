from collections import deque

# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        level, output = 0, []

        if not root:
            return output

        queue = deque([root])

        while queue:
            # We need to add nodes at idx level (e.g., for the root node, at idx = 0)
            # So if the len(output) is equal to level, we need to add a new array to the output
            if len(output) == level:
                output.append([])
            
            # How many elements are there to process at this level? The current length of the queue
            # (e.g., at the root node, there is only one element to process; next, only n children of the root)
            for _ in range(0, len(queue)):
                # Get the next node from the queue
                curr = queue.popleft()
                # Append its value to the output array (at the appropriate level)
                output[level].append(curr.val)

                # Add each of its children to the back of the queue (these won't be processed at this level!)
                if curr.left:
                    queue.append(curr.left)
                if curr.right:
                    queue.append(curr.right)
                
            # At this point, we've reached the next level
            level += 1
        
        return output