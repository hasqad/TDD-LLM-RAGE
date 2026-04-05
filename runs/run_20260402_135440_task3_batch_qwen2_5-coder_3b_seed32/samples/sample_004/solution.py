from typing import List

def is_valid(s: str) -> bool:
    stack = []
    matching_brackets = {')': '(', '}': '{', ']': '['}
    
    for char in s:
        if char in matching_brackets.values():
            stack.append(char)
        elif char in matching_brackets.keys():
            if not stack or stack.pop() != matching_brackets[char]:
                return False
        else:
            # In case of an unexpected character, consider it invalid
            return False
    
    return len(stack) == 0