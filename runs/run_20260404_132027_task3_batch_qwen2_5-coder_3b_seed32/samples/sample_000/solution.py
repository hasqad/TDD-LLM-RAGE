def is_valid(s: str) -> bool:
    stack = []
    matching_brackets = {')': '(', '}': '{', ']': '['}
    
    for char in s:
        if char in matching_brackets.values():
            stack.append(char)
        elif char in matching_brackets.keys():
            if not stack or stack[-1] != matching_brackets[char]:
                return False
            stack.pop()
        else:
            # In case there's an unexpected character, return False
            return False
    
    return len(stack) == 0