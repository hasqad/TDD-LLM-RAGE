def num_decodings(s: str) -> int:
    if len(s) == 0 or s[0] == '0':
        return 0
    
    dp = [1] + [0] * len(s)
    
    for i in range(1, len(s)):
        if s[i] != '0':
            dp[i + 1] += dp[i]
        
        if i > 0 and (s[i-1] == '1' or (s[i-1] == '2' and int(s[i]) <= 6)):
            dp[i + 1] += dp[i - 1]
    
    return dp[-1]