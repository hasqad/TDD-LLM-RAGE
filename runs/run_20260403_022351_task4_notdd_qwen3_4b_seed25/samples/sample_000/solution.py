def min_distance(word1: str, word2: str) -> int:
    m = len(word1)
    n = len(word2)
    dp_prev = list(range(n + 1))
    for i in range(m):
        dp_curr = [0] * (n + 1)
        dp_curr[0] = i + 1
        for j in range(n):
            if word1[i] == word2[j]:
                dp_curr[j + 1] = dp_prev[j]
            else:
                dp_curr[j + 1] = 1 + min(dp_prev[j + 1], dp_curr[j], dp_prev[j])
        dp_prev = dp_curr
    return dp_prev[n]