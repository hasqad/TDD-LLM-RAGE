def min_distance(word1: str, word2: str) -> int:
    m, n = len(word1), len(word2)
    
    if m > n:
        return min_distance(word2, word1)
    
    prev_row = [0] * (n + 1)
    curr_row = [0] * (n + 1)
    
    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0:
                curr_row[j] = j
            elif j == 0:
                curr_row[j] = i
            elif word1[i - 1] == word2[j - 1]:
                curr_row[j] = prev_row[j - 1]
            else:
                replace_cost = 1 + min(prev_row[j], curr_row[j - 1])
                insert_cost = 1 + curr_row[j - 1]
                delete_cost = 1 + prev_row[j - 1]
                curr_row[j] = min(replace_cost, insert_cost, delete_cost)
        prev_row, curr_row = curr_row, prev_row
    
    return prev_row[-1]