def recipe_chain_optimization(n: int, recipes: list, graph: list, min_cal: int, min_protein: int) -> int:
    if n == 0:
        return 0
    
    costs = [r[1] for r in recipes]
    cal = [r[2][0] for r in recipes]
    prot = [r[2][1] for r in recipes]
    parent_set = [set(graph[i]) for i in range(n)]
    
    max_cal = 2000
    max_prot = 2000
    
    dp = [[float('inf')] * (max_prot + 1) for _ in range(max_cal + 1)]
    
    for mask in range(1 << n):
        valid = True
        for i in range(n):
            if mask & (1 << i):
                for p in parent_set[i]:
                    if not (mask & (1 << p)):
                        valid = False
                        break
                if not valid:
                    break
                    
        if not valid:
            continue
            
        total_cal_val = 0
        total_prot_val = 0
        total_cost_val = 0
        for i in range(n):
            if mask & (1 << i):
                total_cal_val += cal[i]
                total_prot_val += prot[i]
                total_cost_val += costs[i]
                
        if total_cal_val <= max_cal and total_prot_val <= max_prot:
            if total_cost_val < dp[total_cal_val][total_prot_val]:
                dp[total_cal_val][total_prot_val] = total_cost_val
                
    ans = float('inf')
    for c in range(min_cal, max_cal + 1):
        for p in range(min_protein, max_prot + 1):
            if dp[c][p] < ans:
                ans = dp[c][p]
                
    return ans