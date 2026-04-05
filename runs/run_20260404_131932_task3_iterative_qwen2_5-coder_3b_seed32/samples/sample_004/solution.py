def is_valid(s: str) -> bool:
    stack = []
    matching_brackets = {') : '(', '}': '{', ']': '['}
    
    for char in s:
        if char in matching_brackets.values():
            stack.append(char)
        elif char in matching_brackets.keys() and (not stack or stack[-1] != matching_brackets[char]):
            return False
        else:
            stack.pop()
    
    return len(stack) == 0