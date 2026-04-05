def is_valid(s: str) -> bool:
    stack = []
    closing_to_open = {')': '(', ']': '[', '}': '{'}
    for char in s:
        if char in ['(', '[', '{']:
            stack.append(char)
        else:
            if not stack:
                return False
            top = stack.pop()
            if top != closing_to_open[char]:
                return False
    return len(stack) == 0