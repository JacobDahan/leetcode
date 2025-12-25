# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def inorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        if root is None:
            return []
        
        # DFS demands that we use a STACK to track what work remains (last-in, first-out)
        # In-order traversal means that the root is IN-between left and right nodes
        # So, for every node, we must go left as far as possible before processing the root
        # After processing the root, we can look right
        node, stack, output = root, [], []
        while node or stack:
            # Traverse the tree left-wards
            while node:
                stack.append(node)
                node = node.left
            
            # At this point, `node` must be `None`, so grab the next
            # (either `node` started as `Some` and was thus appended to the stack or stack started as non-empty)
            node = stack.pop()

            # Store the value of this node
            output.append(node.val)

            # ... And process its right child
            node = node.right
        
        return output

    # def inorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
    #     if root is None:
    #         return []
        
    #     # DFS demands that we use a STACK to track what work remains (last-in, first-out)
    #     stack, output = [root], []

    #     while stack:
    #         node = stack.pop()

    #         # If node is None, we've reached the end of the road on this branch
    #         if node is None:
    #             continue

    #         # in-order traversal means we process left, then val, then right
    #         # because of the stack data structure, this requires that we push right-before-left (last-in, first-out)
    #         if node.right or node.left:
    #             stack.append(node.right)
    #             # we can force val to be processed between left and right by adding a "leaf-ish" node to the stack
    #             stack.append(TreeNode(node.val))
    #             stack.append(node.left)
    #         else:
    #             output.append(node.val)

    #     return output
        # Recursion is trivial, iterables are forever
        # return self.inorderTraversal(root.left) + [root.val] + self.inorderTraversal(root.right)