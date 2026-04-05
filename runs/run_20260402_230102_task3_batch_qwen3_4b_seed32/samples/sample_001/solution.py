def is_valid(s: str) -> bool:
    stack = []
    mapping = {')': '(', '}': '{', ']': '['}
    for c in s:
        if c in mapping:
            if not stack:
                return False
            if stack.pop() != mapping[c]:
                return False
        else:
            stack.append(c)
    return not stack