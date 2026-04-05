def is_valid(s: str) -> bool:
    stack = []
    mapping = {')': '(', '}': '{', ']': '['}
    for char in s:
        if char in '([{':
            stack.append(char)
        else:
            if not stack:
                return False
            if mapping[char] != stack.pop():
                return False
    return not stack