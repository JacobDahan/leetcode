# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right


class Solution:
    def postorderTraversal(self, root):
        if not root:
            return []
        
        curr, stack, output = root, [], []
        previous = None

        while curr or stack:
            # either curr is some or stack is non-empty

            # if curr is some, look leftwards
            while curr:
                stack.append(curr)
                curr = curr.left

            # at this point, the stack must be non-empty
            curr = stack.pop()

            # if we *can* go right, we must (unless we already have!)
            if curr.right and curr.right != previous:
                stack.append(curr)
                curr = curr.right
            # otherwise, we are finally ready to process this node
            else:
                output.append(curr.val)
                # in case this was the right-child, make sure that we mark this as previous
                previous = curr
                # and unset curr so that we don't re-process the same
                curr = None
        
        return output