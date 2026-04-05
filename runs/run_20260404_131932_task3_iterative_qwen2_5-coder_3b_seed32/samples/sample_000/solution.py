def is_valid(s: str) -> bool:
    stack = []
    pairs = {') : '(', '}': '{', ']': '['}
    
    for char in s:
        if char in pairs.values():
            stack.append(char)
        elif char in pairs.keys():
            if not stack or stack.pop() != pairs[char]:
                return False
        else:
            # In case of an unexpected character, which should not happen given the problem constraints
            return False
    
    return len(stack) == 0