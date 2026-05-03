def num_decodings(s: str) -> int:
    n = len(s)
    # If the string is empty, return 0 (though the constraint says at least length 1, but handling for completeness)
    if n == 0:
        return 0
    dp = [0] * (n + 1)
    dp[0] = 1  # base case: empty string has 1 way
    # If the first character is '0', then there's no valid way for the first character
    dp[1] = 1 if s[0] != '0' else 0
    for i in range(2, n + 1):
        dp[i] = 0
        # If the current digit is not '0', we can take it as a single digit
        if s[i - 1] != '0':
            dp[i] += dp[i - 1]
        # Check the two-digit number ending at i
        two_digit = int(s[i - 2:i])
        if 10 <= two_digit <= 26:
            dp[i] += dp[i - 2]
    return dp[n]