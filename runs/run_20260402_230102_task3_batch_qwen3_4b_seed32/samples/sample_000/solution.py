def is_valid(s: str) -> bool:
    stack = []
    closing_to_opening = {')': '(', ']': '[', '}': '{'}
    
    for c in s:
        if c in ['(', '[', '{']:
            stack.append(c)
        else:
            if not stack:
                return False
            top = stack.pop()
            if top != closing_to_opening[c]:
                return False
    
    return len(stack) == 0