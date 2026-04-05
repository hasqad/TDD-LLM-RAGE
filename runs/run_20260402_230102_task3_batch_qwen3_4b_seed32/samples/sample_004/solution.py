def is_valid(s: str) -> bool:
    stack = []
    mapping = {')': '(', '}': '{', ']': '['}
    for c in s:
        if c in mapping.values():
            stack.append(c)
        else:
            if not stack:
                return False
            if stack[-1] != mapping[c]:
                return False
            stack.pop()
    return len(stack) == 0