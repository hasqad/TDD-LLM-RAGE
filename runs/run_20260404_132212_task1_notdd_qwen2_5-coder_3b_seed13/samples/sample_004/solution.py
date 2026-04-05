def num_decodings(s: str) -> int:
    if not s or s[0] == '0':
        return 0
    
    dp = [1] + [0] * len(s)
    
    for i in range(1, len(s)):
        # Single digit decoding
        if s[i] != '0':
            dp[i] += dp[i - 1]
        
        # Two-digit decoding
        if (i > 0 and '1' <= s[i-1:i+1] <= '26'):
            dp[i] += dp[i - 2]
    
    return dp[-1]

# Example usage:
print(num_decodings('226'))  # Output: 3