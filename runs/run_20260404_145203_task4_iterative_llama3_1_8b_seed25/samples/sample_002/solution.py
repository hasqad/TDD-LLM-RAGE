def min_distance(word1: str, word2: str) -> int:
    m, n = len(word1), len(word2)
    
    # Create a 2D array to store the minimum distance between substrings of word1 and word2
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # Initialize the first row and column with increasing integers, representing insertions and deletions
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    
    # Fill in the rest of the array using dynamic programming
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            cost = 0 if word1[i - 1] == word2[j - 1] else 1
            dp[i][j] = min(dp[i - 1][j] + 1, dp[i][j - 1] + 1, dp[i - 1][j - 1] + cost)
    
    # The minimum distance is stored in the bottom-right corner of the array
    return dp[m][n]