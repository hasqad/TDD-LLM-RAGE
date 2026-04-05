def is_valid(s: str) -> bool:
    # Dictionary to hold matching pairs of brackets
    bracket_pairs = {')': '(', '}': '{', ']': '['}
    
    # Stack to keep track of opening brackets
    stack = []
    
    for char in s:
        if char in bracket_pairs.values():  # If it's an opening bracket
            stack.append(char)
        elif char in bracket_pairs:  # If it's a closing bracket
            if not stack or stack[-1] != bracket_pairs[char]:
                return False
            stack.pop()
    
    return len(stack) == 0

# Example usage:
print(is_valid('()[]{}'))  # Output: True