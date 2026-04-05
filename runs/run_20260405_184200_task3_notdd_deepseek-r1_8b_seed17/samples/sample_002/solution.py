def recipe_chain_optimization(n: int, recipes: List[Tuple[str, int, Tuple[int, int]]], graph: List[List[int]], min_cal: int, min_protein: int) -> int:
    parent_set = [set(p) for p in graph]
    
    INF = 10**9
    best = [[INF] * (min_protein + 1) for _ in range(min_cal + 1)]
    
    for mask in range(1 << n):
        valid = True
        for i in range(n):
            if mask & (1 << i):
                for parent_index in parent_set[i]:
                    if not (mask & (1 << parent_index)):
                        valid = False
                        break
                if not valid:
                    break
        
        if not valid:
            continue
            
        total_cal = 0
        total_pro = 0
        total_cost = 0
        for i in range(n):
            if mask & (1 << i):
                cal, pro = recipes[i][2]
                cost_i = recipes[i][1]
                total_cal += cal
                total_pro += pro
                total_cost += cost_i
        
        for c in range(min_cal, total_cal + 1):
            for p in range(min_protein, total_pro + 1):
                if best[c][p] > total_cost:
                    best[c][p] = total_cost
    
    return best[min_cal][min_protein]