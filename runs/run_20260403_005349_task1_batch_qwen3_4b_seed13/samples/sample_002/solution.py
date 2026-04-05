def num_decodings(s: str) -> int:
    n = len(s)
    dp = [0] * (n + 1)
    dp[0] = 1
    for i in range(1, n + 1):
        if s[i-1] != '0':
            dp[i] += dp[i-1]
        if i >= 2:
            two_digit = s[i-2:i]
            if two_digit[0] != '0' and 10 <= int(two_digit) <= 26:
                dp[i] += dp[i-2]
    return dp[n]