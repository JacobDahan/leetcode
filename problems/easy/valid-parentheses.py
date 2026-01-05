class Solution:
    def isValid(self, s: str) -> bool:
        # Naive:
        # - Traverse string, filling up a stack as we go
        # - If we encounter a closing symbol, check the top of the stack
        # - The closing symbol must match the top of the stack, else return false
        # - If closing symbol matches, pop from stack and continue
        # - If stack is not empty at end, return false

        # Smarter:
        # - What if there are many duplicates (e.g., "((((((((((()))))))))))")
        # - This will require an immense amount of memory to fill our stack
        # - Instead, keep a stack of `(char, count)`
        # - Decrement the count as needed
        # - On any new character, create a new element in the stack

        stack = []
        close_to_open_map = {
            ')': '(',
            '}': '{',
            ']': '['
        }

        for c in s:
            # If this is a closing character, we must check the top of the stack
            if c in close_to_open_map.keys():
                # If the stack is empty, this is not a valid string definitionally
                if not stack:
                    return False
                
                # Get the latest element from the stack
                last_c, c_count = stack[-1]
                
                # If this doesn't match the expected char, this is not a valid string
                if last_c != close_to_open_map[c]:
                    return False

                # Otherwise, decrement the count...
                stack[-1] = (last_c, c_count - 1)

                # If we have exhausted the open chars of this type, remove it from the stack
                if stack[-1][1] == 0:
                    stack.pop()
            
            else:
                # If the stack is empty, simply append this char and its count
                if not stack:
                    stack.append((c, 1))
                    continue

                # Otherwise, get the latest value from the stack
                last_c, c_count = stack[-1]

                if last_c != c:
                    # If the chars don't match, add the new value to the stack
                    stack.append((c, 1))
                else:
                    # Otherwise, increment the count
                    stack[-1] = (last_c , c_count + 1)
            
        # If there is anything left in our stack, this isn't a valid string
        return len(stack) == 0
