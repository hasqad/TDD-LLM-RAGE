def is_valid(s: str) -> bool:
    stack = []
    closing_map = {')': '(', '}': '{', ']': '['}
    for char in s:
        if char in ['(', '{', '[']:
            stack.append(char)
        else:
            if not stack:
                return False
            top = stack.pop()
            if top != closing_map[char]:
                return False
    return len(stack) == 0