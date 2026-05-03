def num_decodings(s: str) -> int:
    n = len(s)
    if n == 0:
        return 0
    dp = [0] * (n + 1)
    dp[0] = 1
    if s[0] == '0':
        dp[1] = 0
    else:
        dp[1] = 1
    for i in range(2, n + 1):
        two_digit_valid = (s[i-2] == '1') or (s[i-2] == '2' and s[i-1] <= '6')
        if s[i-1] != '0':
            dp[i] = dp[i-1]
            if two_digit_valid:
                dp[i] += dp[i-2]
        else:
            if two_digit_valid:
                dp[i] = dp[i-2]
            else:
                dp[i] = 0
    return dp[n]