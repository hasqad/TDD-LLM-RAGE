import re

def is_palindrome(s: str) -> bool:
    # Normalize the string by removing non-alphanumeric characters and converting to lowercase
    normalized = re.sub(r'[^a-zA-Z0-9]', '', s).lower()
    
    # Check if the normalized string reads the same forwards and backwards
    return normalized == normalized[::-1]