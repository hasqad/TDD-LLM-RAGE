from collections import deque

def is_valid(s: str) -> bool:
    stack = deque()
    
    for char in s:
        if char == '(' or char == '{' or char == '[':
            stack.append(char)
        else:
            if not stack:
                return False
            
            top = stack.pop()
            
            if (char == ')' and top != '(') or \
               (char == '}' and top != '{') or \
               (char == ']' and top != '['):
                return False
    
    return len(stack) == 0