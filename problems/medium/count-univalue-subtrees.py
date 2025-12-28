# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def countUnivalSubtrees(self, root: Optional[TreeNode]) -> int:
        # Thoughts:
        # - Because we need to explore node-to-leaf, this sounds like a DFS problem
        # - Technically, we need to visit every node, so this would be solvable by BFS, too
        # - However, it'll be hard enough to track what we need to track for just one branch at a time,
        #   so we can skip some extra bookkeeping by sticking with DFS
        # - What is a unival subtree? A uni-value subtree means all nodes of the subtree have the same value.
        #   - Simplest case: A leaf node
        #   - Next simplest case: A node with one or more leaf node children of the same value
        # - How can we determine if a node is the root of a unival subtree?
        #   - We can recursively (top down) walk a branch of the tree, keeping track of what our
        #     "search value" is and returning a tuple of (is_unival, count_unival)
        if not root:
            return 0
        
        _, count = self.checkUnivalSubtree(root, root.val)
        return count

    def checkUnivalSubtree(self, root: Optional[TreeNode], value: int) -> Tuple[bool, int]:
        if not root:
            # If the node doesn't exist, it definitinally is not a unival subtree, but does not
            # invalidate an otherwise unival subtree
            return (True, 0)

        # Determine if left and right trees (a) make this a unival node and (b) contain unival subtrees
        l_is_unival, l_unival_count = self.checkUnivalSubtree(root.left, root.val)
        r_is_unival, r_unival_count = self.checkUnivalSubtree(root.right, root.val)

        # Count the total number of unival subtrees (L child unival trees, R child unival trees, plus this tree,
        # IFF the children match this value)
        children_match_unival = l_is_unival and r_is_unival
        unival_subtree_count = l_unival_count + r_unival_count + (1 if children_match_unival else 0)

        # Finally, tell the parent node if *it* is unival along with the total 
        # number of unival subtrees it contains
        return (children_match_unival and root.val == value, unival_subtree_count)
