from typing import Optional, Tuple

"""
The thief has found himself a new place for his thievery again. There is only one entrance to this area, called root.

Besides the root, each house has one and only one parent house. After a tour, the smart thief realized that all houses in this place form a binary tree. It will automatically contact the police if two directly-linked houses were broken into on the same night.

Given the root of the binary tree, return the maximum amount of money the thief can rob without alerting the police.
"""

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    """
    Task:
    - We are asked to write a method `rob` that returns the MAXIMUM amount of money that can be robbed from a BINARY TREE with root `root`
    - There exists a CONSTRAINT that we cannot rob directly-linked (i.e., parent-child) houses

    Observations:
    - Because trees are naturally recursive, we might consider a recursive Solution
    - Because there exists a CONSTRAINT whereby previous decisions impact future decisions (i.e., robbing node i means it is not possible to rob node i.left),
      greedy algorithms are provably incorrect
    - As we start to build out the recursive algorithm, we should keep an eye for repeating sub-problems that can be memoized (IF ANY EXIST)

    Algorithm:
    - We can generalize the question to ask "what is the maximum amount that can be robbed from a tree with root `node`?"
        - The trivial answer to this is:
            - Either the maximum that can be robbed in each of its children, combined
            - OR the maximum that can be robbed in each of its grand-children, combined, PLUS the value of this house
        - In this case, the base case is trivial:
            - If a node has no children, the maximum that can be robbed is certain to be the value of that house
        - In other words:
            - At every node, we can either rob this node, or not rob this node
            - If we rob this node, we must not rob the children
            - If we do not rob this node, we may (or may not!!) rob the children, whatever is most optimal
    - However, if we start thinking about our function signature (def rob_recursive(root) -> ?), we realize that it is not clear what to return:
        - If we return the maximum robbable at the child, we have no way of knowing if that came from robbing the child node or not!
        - We could dive deeper into the tree and check grand-children, but that would be messy...
        - We could update our signature to call with a boolean distinguishing calls where we robbed the parent or did not, but that leads to duplicate work...
        - Instead, we could update our RETURN VALUE to a tuple of (tree_max, tree_max_without_robbing_root)
    - This is effectively just depth first search! We traverse every node in the tree recursively to determine the maximum robbable amount for every given sub-tree
        - Because we visit every node exactly once, this is an O(n) algorithm and there is no repeating sub-problem (no memoization needed)
        - In the worst case, the tree will be a straight line (completely unbalanced), in which case our call stack will be the height of the tree n, so
          we take O(n) space complexity
    """
    def rob(self, root: Optional[TreeNode]) -> int:
        def rob_recursive(root: Optional[TreeNode]) -> Tuple[int, int]:
            """
            Utility method to determine the maximum amount robbable from a tree with root `root`.

            Returns a tuple of:
            1. The maximum amount robbable from the tree.
            2. The maximum amount robbable from the tree WITHOUT robbing the root node.

            Note that these can be equivalent, in the case that it is not optimal to rob the root node.
            """
            # base cases
            if not root:
                return (0, 0) # no node exists; there is no value here, and there is no value in the children
            elif not root.left and not root.right:
                return (root.val, 0) # this is a leaf node; there is no value in any of the children, and the maximal value of a tree with this root is clearly to rob this houses
            
            left_root_max, left_skip_root = rob_recursive(root.left)
            right_root_max, right_skip_root = rob_recursive(root.right)

            # first, calculate the maximum value attainable at this node
            # this is definitionally the maximum of the two children, OR the sum of the maximum robbably amount SKIPPING those children and robbing this house
            node_max = max(
                left_skip_root + right_skip_root + root.val, # if we rob root.val, we MUST NOT rob the children, but MAY rob the grand-children
                left_root_max + right_root_max, # if we do not rob root.val, we can take the ABSOLUTE MAXIMUM value attainable from the children, whether or not that involves robbing them
            )

            return (
                node_max, # the maximum value attainable at this node, possibly including robbing it
                left_root_max + right_root_max, # the maximum value attainable at the children of this node, NOT robbing this node
            )
        
        node_max, _ = rob_recursive(root) # this returns both the maximum of this tree AND the maximum without robbing the root; we only care about the absolute maximum
        return node_max

import pytest

worst_case = TreeNode( # tree 1 --> 2 --> 3 --> 4 (expected = 6)
    val = 1,
    left = TreeNode(
        val = 2,
        left = TreeNode(
            val = 3,
            left = TreeNode(
                val = 4
            )
        )
    )
)

balanced = TreeNode( # tree [3,2,3,null,3,null,1] (expected = 7)
    val = 3,
    left = TreeNode(
        val = 2,
        right = TreeNode(
            val = 3
        )
    ),
    right = TreeNode(
        val = 3,
        right = TreeNode(
            val = 1
        )
    )
)

empty = None # null tree (expected = 0)

single = TreeNode( # root-only tree (expected = 100)
    val = 100
)

not_greedy = TreeNode( # non-local maximum tree (expected = 10)
    val = 6,
    left = TreeNode(
        val = 5
    ),
    right = TreeNode(
        val = 5
    )
)

@pytest.mark.parametrize(
    "root,expected",
    [
        (worst_case, 6),
        (balanced, 7),
        (empty, 0),
        (single, 100),
        (not_greedy, 10),
    ]
)
def test_rob(root, expected):
    s = Solution()
    a = s.rob(root)
    assert a == expected, f"Expected {expected}, observed {a}"

if __name__ == "__main__":
    pytest.main(['-v', '-s'])