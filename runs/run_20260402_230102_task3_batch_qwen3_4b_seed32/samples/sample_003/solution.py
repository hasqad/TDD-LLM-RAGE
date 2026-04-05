def is_valid(s: str) -> bool:
    stack = []
    mapping = {')': '(', ']': '[', '}': '{'}
    for char in s:
        if char in mapping.values():
            stack.append(char)
        else:
            if not stack:
                return False
            top = stack.pop()
            if mapping[char] != top:
                return False
    return len(stack) == 0