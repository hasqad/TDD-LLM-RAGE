def is_valid(s: str) -> bool:
    mapping = {')': '(', ']': '[', '}': '{'}
    stack = []
    for char in s:
        if char in mapping.values():
            stack.append(char)
        elif char in mapping.keys():
            if not stack:
                return False
            top = stack.pop()
            if top != mapping[char]:
                return False
    return len(stack) == 0