def num_decodings(s: str) -> int:
    n = len(s)
    dp = [0] * (n+1)
    dp[0] = 1
    for i in range(1, n+1):
        if s[i-1] != '0':
            dp[i] = dp[i-1]
        if i >= 2:
            if s[i-2] == '1' or (s[i-2] == '2' and s[i-1] in '0123456'):
                dp[i] += dp[i-2]
    return dp[n]