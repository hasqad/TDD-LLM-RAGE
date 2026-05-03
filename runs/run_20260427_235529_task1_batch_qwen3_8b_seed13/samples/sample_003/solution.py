def num_decodings(s: str) -> int:
    n = len(s)
    dp = [0] * (n + 1)
    dp[0] = 1
    if s[0] == '0':
        dp[1] = 0
    else:
        dp[1] = 1
    for i in range(2, n + 1):
        if s[i-1] != '0':
            dp[i] += dp[i-1]
        two_digit = s[i-2:i]
        if 10 <= int(two_digit) <= 26:
            dp[i] += dp[i-2]
    return dp[n]