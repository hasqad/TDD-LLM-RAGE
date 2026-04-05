def is_palindrome(s: str) -> bool:
    # Normalize the string by converting it to lowercase and removing non-alphanumeric characters
    normalized_s = ''.join(char.lower() for char in s if char.isalnum())
    
    # Check if the normalized string reads the same forwards and backwards
    return normalized_s == normalized_s[::-1]