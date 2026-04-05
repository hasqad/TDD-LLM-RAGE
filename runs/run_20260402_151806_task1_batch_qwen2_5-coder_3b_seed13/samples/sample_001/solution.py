def num_decodings(s: str) -> int:
    if not s or s[0] == '0':
        return 0
    
    dp = [1] + [0] * len(s)
    
    for i in range(1, len(s)):
        if s[i] != '0':
            dp[i] += dp[i - 1]
        
        if (s[i-1:i+1] >= '10' and s[i-1:i+1] <= '26'):
            dp[i] += dp[i - 2]
    
    return dp[-1]